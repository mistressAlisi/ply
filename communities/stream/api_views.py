import io

from django.core.exceptions import PermissionDenied
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PIL import Image
import datetime
from django.db import transaction
# Ply:
from communities.profiles.models import Profile
from communities.community.forms import CommunityForm
from communities.stream.ejabberapictl.rest import RESTAPIClient
from ply import settings,system_uuids
from ply.toolkit import vhosts,profiles, file_uploader,groups,reqtools
from core.dynapages.models import Templates,Page, PageWidget
from ply.toolkit.contexts import default_context
from ply.toolkit.roles import is_profile_admin
from roleplaying.stats.models import BaseStat,ProfileStat
from communities.community.models import Community,CommunityProfile,CommunityAdmins
from communities.stream.forms import StreamSettingsForm,CreateStreamForm
from communities.stream.models import Stream, StreamMessage, StreamXMPPSettings, StreamProfileXMPPSettings, \
    StreamProfileXMPPMUCs


# Create your views here.

# Upload an avatar and apply it to the currently specified profile in the session space:
@login_required
def set_profile_settings(request):
    community = Community.objects.get(uuid=request.session['community'])
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    if request.method == 'POST':
                profile = Profile.objects.get(uuid=request.session['profile'])
                try:
                    stream = Stream.objects.get_or_create(community=community,profile=profile,root_stream=True,type="PROFILE")[0]
                    stream.group = groups.get_placeholder()
                    f = StreamSettingsForm(request.POST,instance=stream)
                    f.save()
                    print("saved")
                except Exception as e:
                    print('ERROR: Cannot save Profile Stream:')
                    print(profile)
                    print(f.errors)
                    return JsonResponse({"res":"ERR","data":f.errors},safe=False)  
                return JsonResponse({"res":"ok"},safe=False)  
            
    return JsonResponse({"res":"data?"},safe=False)   



# Publish to a specific profile's primary stream:
@login_required
@transaction.atomic
def publish_to_profile(request,profile):
    """
    @brief Publish A POST to a specific profile's primary stream:..
    :param request: p_request:Django Request
    :type request: t_request:str
    :param profile: p_profile:Profile Slug ID
    :type profile: undefined
    :returns: r JSON error object or rendered Stream card
    """
    community = reqtools.vhost_community_or_404(request)
    profile = get_object_or_404(Profile,profile_id=profile)
    author = profiles.get_active_profile(request)

    stream = Stream.objects.get(community=community,profile=profile,root_stream=True,type="PROFILE")
    stream.nodes += 1
    stream.save()
    msg_text = request.POST["contents_text"]
    msg_type = request.POST["type"]
    message = StreamMessage(stream=stream,author=author,type=msg_type,contents_text=msg_text)
    message.save()
    #For the author's stream - if we're posting in streams other than the ones we own...:
    if (author != profile):
        author_stream = Stream.objects.get_or_create(community=community,profile=author,root_stream=True,type="PROFILE")[0]
        author_stream.nodes += 1
        referenceMessage = StreamMessage(stream=author_stream,author=author,type='application/ply.stream.refmsg',references=message,posted_in=stream)
        referenceMessage.save() 
    return JsonResponse({"res":"ok","uuid":message.uuid},safe=False)


# FINISH the currently enabled profile in session space:
# This system call only works on PLACEHOLDER Profiles, it will init a profile's dynapage template, copy it's poulation
# from the default in the system, and remove the placeholder flag.
# THIS WILL NOT WORK on active profiles for obvious reasons:
@login_required
def finish_character_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if (community.restricted is True):
        return JsonResponse({"res":"err","e":"Community is in restricted-join."},safe=False)          
    profile = Profile.objects.get(uuid=request.session['profile'])
    if (profile.placeholder is False):
        return JsonResponse({"res":"err","e":"Profile is not a placeholder."},safe=False)  
    page = Page.objects.get(page_id=system_uuids.profile_dynapage_uuid)
    page.pk = None
    page.slug = f"profile||{request.user}||{profile.profile_id}"
    page.label = f"Profile page for {profile.name}"
    page.save()
    widgets = PageWidget.objects.filter(page_id=system_uuids.profile_dynapage_uuid)
    for widget in widgets:
        widget.pk = None
        widget.page_id = page.page_id
        widget.save()
    profile.dynapage = page

    # Add  stats:
    stats = BaseStat.objects.filter(community=community,archived=False,blocked=False)
    for stat in stats:
        n_stat = ProfileStat.objects.get_or_create(community=community,profile=profile,stat=stat,value=stat.starting,pminimum=stat.minimum,pmaximum=stat.maximum)[0]
        n_stat.save()
    # Join the community! 
    join_comm  = CommunityProfile.objects.get_or_create(community=community,profile=profile,joined=datetime.datetime.utcnow())[0]
    join_comm.save()
    # Finish up:
    profile.placeholder = False    
    profile.save()
    return JsonResponse({"res":"ok"},safe=False)  

# FINISH editing the currently active profile:
# ONLY works on existing, active profiles!
@login_required
def finish_edit_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if (community.restricted is True):
        return JsonResponse({"res":"err","e":"Community is in restricted-join."},safe=False)          
    profile = Profile.objects.get(uuid=request.session['profile'])
    if (profile.placeholder is True):
        return JsonResponse({"res":"err","e":"Profile is a placeholder."},safe=False)  
    profile.updated = datetime.datetime.utcnow()
    profile.save()
    return JsonResponse({"res":"ok"},safe=False)  



# Upload an icon to the Community as an Avatar/cover image:
@login_required
def upload_community_picture(request):
    if 'charImage' not in request.FILES:
        return JsonResponse({"res":"try-again"},safe=False)  
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    if request.method == 'POST':
        file = request.FILES['charImage']
        # Check the file size:
        if (file.size >= settings.PLY_AVATAR_MAX_KB*1024):
                return JsonResponse({"res":"err","e":"Maximum File Size Exceeded"},safe=False)  
        # Check the file type:
        type = file.name.split(".")
        if (len(type) < 2):
                return JsonResponse({"res":"err","e":"Invalid Filetype"},safe=False)  
        if (type[1] not in settings.PLY_AVATAR_FORMATS):
                return JsonResponse({"res":"err","e":"Invalid Filetype"},safe=False)  
        # Now let's thumbnail it and store it in avatar storage:
        with Image.open(file) as im:
                #try:
                im.thumbnail(settings.PLY_AVATAR_MAX_PX)
                avatar_img = io.BytesIO()
                im.save(avatar_img,settings.PLY_AVATAR_IMG_FORMAT)
                path,size = file_uploader.save_avatar_file(avatar_img,community,f"av_{community.uuid}."+type[1])
                #except Exception as e:
                #    print(e)
                #    return JsonResponse({"res":"err","err":"except","e":str(e)},safe=False)
                community.avatar = path 
                community.save()
                return JsonResponse({"res":"ok","path":settings.PLY_AVATAR_FILE_URL_BASE_URL+"/"+path,"size":size},safe=False)
            
    return JsonResponse({"res":"ok"},safe=False)   

# UPDATE the Community profile:
@login_required
def update_community_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    form = CommunityForm(request.POST,instance=community)
    if ('dynapage' in request.POST):
        # Update the Dynapage Template
        dynaPage_Template = request.POST['dynapage']
        template = Templates.objects.get(template_id=dynaPage_Template)
        community.dynapage.template = template
        community.dynapage.save()
    if (not form.is_valid()):
        return JsonResponse({"res":"err","e":str(form.errors.as_data())},safe=False)
    form.save()
    community.save()
    return JsonResponse({"res":"ok"},safe=False)   


# FINISH editing the community:
@login_required
def finish_community_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    community.updated = datetime.datetime.utcnow()
    community.save()
    return JsonResponse({"res":"ok"},safe=False)  

# FINISH editing the community:
@login_required
def create_stream(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    form = CreateStreamForm(request.POST,community=community,profile=profile)
    if (not form.is_valid()):
        return JsonResponse({"res":"err","e":str(form.errors.as_data())},safe=False)
    form.save()
    message = StreamMessage(stream=stream,community=community,type='text/plain',contents_text=f'@{profile.profile_id} created this stream!')
    message.save()
    return JsonResponse({"res":"ok","uuid":form.instance.uuid},safe=False)


@login_required
def xmpp_enroll(request):
    context,vhost,community,profile = default_context(request)
    # Is registration enabled?
    site_settings = StreamXMPPSettings.objects.get_or_create()[0]
    if not site_settings.enabled or not site_settings.self_reg:
        raise PermissionDenied("XMPP and/or self_reg is disabled.")
    # Always the same:
    jid = f"{request.POST['UID']}@{site_settings.domain}"
    # XMPP Services hook:
    xmppctl = RESTAPIClient(community)
    # Update JID pathway:
    if ('update' in request.POST):

        jid_o = StreamProfileXMPPSettings.objects.get(jid=jid)
        if jid_o.community != community or jid_o.profile != profile:
            return JsonResponse({"res": "err", 'code': "400","str":"Access Denied!"}, safe=False)
        xmppctl.update_password(jid_o.get_UID(),site_settings.domain,request.POST['APW'])
        return JsonResponse({"res": "ok"}, safe=False)

    # NOTE: IF YOU UPDATED, YOU SURE AS S* AIN'T HERE!
    # Create JID pathway:

    if len(StreamProfileXMPPSettings.objects.filter(jid=jid)) > 0:
        return JsonResponse({"res": "err",'bad':"jid"}, safe=False)
    try:
        xmppctl.register_jid(request.POST['UID'],site_settings.domain,request.POST['APW'])
    except Exception as e:
        return JsonResponse({"res": "err",'bad':"jid",'e':str(e)}, safe=False)
    # create MUCs:
    if site_settings.auto_group:
        for service,muc,descr in [
            (site_settings.streams,f"__{request.POST['UID']}_saved-msgs",f"{request.POST['UID']}: Saved Messages"),
            (site_settings.streams, f"__{request.POST['UID']}_scratchpad", f"{request.POST['UID']}: Scratchpad"),
            (site_settings.streams, f"__{request.POST['UID']}_cast", f"{request.POST['UID']}: Stream Casting"),
            (site_settings.pubsub, f"__{request.POST['UID']}_pub", f"{request.POST['UID']}: Publish Bridge"),
            (site_settings.pubsub, f"__{request.POST['UID']}_bcast", f"{request.POST['UID']}: Broadcast Bridge"),

        ]:
            xmppctl.register_muc(muc,site_settings.domain,site_settings.streams)
            xmu = StreamProfileXMPPMUCs(name=muc,host=site_settings.domain,service=service,descr=descr)
            xmu.save()

    sp = StreamProfileXMPPSettings.objects.get_or_create(community=community,profile=profile)[0]
    sp.jid = jid
    sp.save()
    return JsonResponse({"res":"ok"},safe=False)
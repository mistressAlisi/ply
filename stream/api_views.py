from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from PIL import Image
import datetime
# Ply:
from profiles.models import Profile
from profiles.forms import ProfileForm
from community.forms import CommunityForm
from ply import settings,system_uuids
from ply.toolkit import vhosts,profiles,logger,file_uploader,groups,reqtools
from dynapages.models import Templates,Page,Widget,PageWidget
from dashboard.navigation import SideBarBuilder
from stats.models import BaseStat,ProfileStat
from community.models import Community,CommunityProfile,CommunityAdmins
from stream.forms import StreamSettingsForm
from stream.models import Stream
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
def publish_to_profile(request,profile):
    community = reqtools.vhost_community_or_404(request)
    profile = get_object_or_404(Profile,profile_id=profile)
    stream_profile = profiles.get_active_profile(request)
    stream = Stream.objects.get(community=community,profile=stream_profile,root_stream=True,type="PROFILE")
    
    form.save()
    profile.save()
    return JsonResponse({"res":"ok"},safe=False)   


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
                path = file_uploader.save_avatar_file(im,community,f"av_{community.uuid}."+type[1])  
                #except Exception as e:
                #    print(e)
                #    return JsonResponse({"res":"err","err":"except","e":str(e)},safe=False)
                community.avatar = path 
                community.save()
                return JsonResponse({"res":"ok","path":settings.PLY_AVATAR_FILE_URL_BASE_URL+"/"+path},safe=False)  
            
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

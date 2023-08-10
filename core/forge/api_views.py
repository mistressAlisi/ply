from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PIL import Image
import datetime
# Ply:
from communities.profiles.models import Profile,ProfilePageNode
from communities.profiles.forms import ProfileForm
from communities.community.forms import CommunityForm
from ply import settings,system_uuids
from ply.toolkit import vhosts,profiles, file_uploader,scripts
from core.dynapages.models import Templates,Page, PageWidget
from roleplaying.stats.models import BaseStat,ProfileStat,ProfileStatHistory
from communities.community.models import Community,CommunityProfile,CommunityAdmins
from core.forge.forms import SaveScriptForm
from core.plyscript.models import Script
from roleplaying.stats.models import ClassType
from roleplaying.exp.models import ProfileExperience,Level
# Create your views here.

# Upload an avatar and apply it to the currently specified profile in the session space:
@login_required
def upload_profile_picture(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if 'charImage' not in request.FILES:
        return JsonResponse({"res":"try-again"},safe=False)  
    profile = Profile.objects.get(uuid=request.session['profile'])
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
                path = file_uploader.save_avatar_file(im,profile,f"av_{profile.uuid}."+type[1])  
                #except Exception as e:
                #    print(e)
                #    return JsonResponse({"res":"err","err":"except","e":str(e)},safe=False)
                profile.avatar = path 
                profile.save()
                return JsonResponse({"res":"ok","path":settings.PLY_AVATAR_FILE_URL_BASE_URL+"/"+path},safe=False)  
            
    return JsonResponse({"res":"ok"},safe=False)   



# UPDATE the currently enabled profile in session space with the provided data from the form:
@login_required
def update_character_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = Profile.objects.get(uuid=request.session['profile'])
    # Save the Dynapage node before update:
    old_dynapage = profile.dynapage
    form = ProfileForm(request.POST,instance=profile)
    if (not form.is_valid()):
        return JsonResponse({"res":"err","e":str(form.errors.as_data())},safe=False)
    form.save()
    if (old_dynapage is not False):
        profile.dynapage = old_dynapage
    profile.save()
    # Update the class data if it's present:
    if 'classtype' in request.POST:
        _classtype = request.POST['classtype']
        classtype = ClassType.objects.get(uuid=_classtype)
        stlevel = Level.objects.get(level=0)
        peo = ProfileExperience.objects.get_or_create(community=community,profile=profile,classtype=classtype,level=stlevel)[0]
        peo.classtype = classtype
        peo.save()
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
    # Create Dynapage nodes and apply them to the profile:
    page = Page.objects.get(page_id=system_uuids.profile_dynapage_uuid)
    page.pk = None
    page.slug = f"profile||{request.user}||{profile.profile_id}"
    page.label = f"Profile page for {profile.name}"
    page.save()
    dpage = Page.objects.get(page_id=system_uuids.pdashboard_dynapage_uuid)
    dpage.pk = None
    dpage.slug = f"profile_dashboard||{request.user}||{profile.profile_id}"
    dpage.label = f"Profile Dashboard page for {profile.name}"
    dpage.save()
    widgets = PageWidget.objects.filter(page_id=system_uuids.profile_dynapage_uuid)
    for widget in widgets:
        widget.pk = None
        widget.page_id = page.page_id
        widget.save()
    # Create Page Nodes in the Dynapage System:
    profile_node = ProfilePageNode(profile=profile,dynapage=page,node_type="profile")
    profile_node.save()
    profile_node = ProfilePageNode(profile=profile,dynapage=dpage,node_type="dashboard")
    profile_node.save()

    # Add  stats:
    stats = BaseStat.objects.filter(community=community,archived=False,blocked=False)
    for stat in stats:
        n_stat = ProfileStat.objects.get_or_create(community=community,profile=profile,stat=stat,value=stat.starting,pminimum=stat.minimum,pmaximum=stat.maximum)[0]
        n_stat.save()
        n_stat_h = ProfileStatHistory.objects.get_or_create(community=community,profile=profile,stat=stat,value=stat.starting,pminimum=stat.minimum,pmaximum=stat.maximum,notes="Added by the Forge during Chargen.")[0]
        n_stat_h.save()
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


# Evaluate a script from scriptStudio:
@login_required
def script_studio_eval(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    code_body = request.POST['code_body']
    pid = request.POST['profile']
    cid = request.POST['community']
    pro = Profile.objects.get(pk=pid)
    com = Community.objects.get(pk=cid)
    try:
           ret = scripts.exec_script_str(com,pro,code_body)
    except Exception as e:
            return JsonResponse({"res":"err",'out':f"<strong>*ERROR:* {str(e)}.</strong><br/>"},safe=False)
    ret = ret.replace("\n","<br/>")
    return JsonResponse({"res":"ok",'out':ret},safe=False)


# Save a script from scriptStudio:
@login_required
def script_studio_save(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    function_name = request.POST['function_name']
    scriptObj = Script.objects.get_or_create(function_name=function_name,community=community,creator=profile.creator)[0]
    form_saver = SaveScriptForm(request.POST,instance=scriptObj)
    if (not form_saver.is_valid()):
        return JsonResponse({"res":"err","e":str(form_saver.errors.as_data())},safe=False)
    form_saver.save()
    return JsonResponse("ok",safe=False)

@login_required
def script_studio_get(request,script):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    scriptObj = Script.objects.get(pk=script)
    return JsonResponse({'res':"ok",'data':scriptObj.body},safe=False)

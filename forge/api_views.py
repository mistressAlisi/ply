from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from PIL import Image
# Ply:
from profiles.models import Profile
from profiles.forms import ProfileForm
from ply import settings,system_uuids
from ply.toolkit import vhosts,profiles,logger,file_uploader
from dynapages.models import Templates,Page,Widget,PageWidget
from dashboard.navigation import SideBarBuilder
# Create your views here.

# Upload an avatar and apply it to the currently specified profile in the session space:
@login_required
def upload_profile_picture(request):
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
                return JsonResponse({"res":"ok","path":settings.PLY_AVATAR_FILE_URL_BASE_URL+path},safe=False)  
            
    return JsonResponse({"res":"ok"},safe=False)   



# UPDATE the currently enabled profile in session space with the provided data from the form:
@login_required
def update_character_profile(request):
    profile = Profile.objects.get(uuid=request.session['profile'])
    form = ProfileForm(request.POST,instance=profile)
    if (not form.is_valid()):
        return JsonResponse({"res":"err","e":str(form.errors.as_data())},safe=False)  
    form.save()
    return JsonResponse({"res":"ok"},safe=False)   


# FINISH the currently enabled profile in session space:
# This system call only works on PLACEHOLDER Profiles, it will init a profile's dynapage template, copy it's poulation
# from the default in the system, and remove the placeholder flag.
# THIS WILL NOT WORK on active profiles for obvious reasons:
@login_required
def finish_character_profile(request):
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
    profile.placeholder = False    
    profile.save()
    return JsonResponse({"res":"ok"},safe=False)  

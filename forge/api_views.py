from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from ply.toolkit import vhosts,profiles,logger,file_uploader
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
# Create your views here.

# Render the Create Profile Forge Page:
@login_required
def upload_profile_picture(request):

    profile = Profile.objects.get(uuid=request.session['profile'])
    if request.method == 'POST':
        file = request.FILES['charImage']
        type = file.name.split(".")
        if (len(type) < 2):
                return JsonResponse({"err":"type"},safe=False)  
       
        #relpath = file_uploader.save_temp_file(file,profile)
    return JsonResponse("ok",safe=False)   

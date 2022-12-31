from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

import ply
from ply.toolkit import vhosts,profiles
from community.models import Friend_ExpLvl_View
from profiles.models import Profile


# Create your views here.

# Render the User Dashboard Home page:
@login_required
def all_friends(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    friends1 = Friend_ExpLvl_View.objects.filter(friend1_id=profile.uuid)
    friends2 = Friend_ExpLvl_View.objects.filter(friend2_id=profile.uuid)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'friends1':friends1,'friends2':friends2}
    return render(request,"community/dashboard/friend_index.html",context)


@login_required
def all_mentions(request):

    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"notifications-all_mentions.html",context)
    #return JsonResponse(colls,safe=False)   



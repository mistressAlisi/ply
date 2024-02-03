from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from communities.profiles.models import Profile
import ply
from media.gallery.core import serialisers
# Create your views here.

# Render the User Dashboard Home page:
@login_required
def all_notifications(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"core-dashboard_list.html",context)


@login_required
def all_mentions(request):
    colls = serialisers.serialise_profile_collection_items(request)
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"notifications-all_mentions.html",context)
    #return JsonResponse(colls,safe=False)   



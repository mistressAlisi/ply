from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from media.gallery.core.uploader import upload_plugins_builder
from media.gallery.core.models import GalleryTempFile, GalleryItemsByFavourites
from communities.profiles.models import Profile
import ply
from media.gallery.core import serialisers
from ply.toolkit.contexts import default_context


# Create your views here.

# Render the User Dashboard Home page:
@login_required
def gallery_list(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"core-dashboard_list.html",context)


@login_required
def upload_content(request):
    context, vhost, community, profile = default_context(request)
    buttons = upload_plugins_builder(community)
    context = {'buttons':buttons.modules.values()}
    return render(request,"media.gallery.core/dashboard/uploader/upload.html",context)

@login_required
def upload_lighttable(request):
    files = GalleryTempFile.objects.filter(profile=request.session['profile'])
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"files":files,"base_url":ply.settings.PLY_TEMP_FILE_URL_BASE_URL,'profile':profile}
    return render(request,"core-dashboard_upload_lighttable.html",context)

@login_required
def gallery_collections(request):
    colls = serialisers.serialise_profile_collection_items(request)
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"core-dashboard_all_collections.html",context)
    #return JsonResponse(colls,safe=False)   

@login_required
def gallery_myfavs(request):
    items = GalleryItemsByFavourites.objects.filter(gif_profile=request.session['profile'])
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"favs":items,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"core/dashboard/gallery_my_likes.html",context)
    #return JsonResponse(colls,safe=False)


@login_required
def gallery_manage(request):
    colls = serialisers.serialise_profile_collection_items(request)
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"core-dashboard_manage_collections.html",context)

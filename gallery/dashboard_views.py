from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts
from gallery.uploader import upload_plugins_builder
from gallery.models import GalleryTempFile,GalleryCollectionItems,GalleryCollection,GalleryItem,GalleryItemFile,GalleryCollectionPermission,GalleryItemsByCollectionPermission
from profiles.models import Profile
from django.http import JsonResponse,HttpResponse
import ply
from gallery import serialisers
# Create your views here.

# Render the User Dashboard Home page:
@login_required
def gallery_list(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    context = {'community':community,'vhost':vhost}
    return render(request,"gallery-dashboard_list.html",context)


@login_required
def upload_content(request):
    buttons = upload_plugins_builder()
    context = {'buttons':buttons.modules.values()}
    return render(request,"gallery-dashboard_upload.html",context)

@login_required
def upload_lighttable(request):
    files = GalleryTempFile.objects.filter(profile=request.session['profile'])
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"files":files,"base_url":ply.settings.PLY_TEMP_FILE_URL_BASE_URL,'profile':profile}
    return render(request,"gallery-dashboard_upload_lighttable.html",context)

@login_required
def gallery_collections(request):
    colls = serialisers.serialise_profile_collection_items(request,True)
    profile = Profile.objects.get(uuid=request.session["profile"])
    context = {"colls":colls,"base_url":ply.settings.PLY_TEMP_FILE_URL_BASE_URL,'profile':profile}
    return render(request,"gallery-dashboard_all_collections.html",context)
    #return JsonResponse(colls,safe=False)   



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from gallery import serialisers
from gallery.models import GalleryCollection
# Render the Gallery Home page:
def gallery_home(request):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        colls = serialisers.serialise_community_items(request)    
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}
        return render(request,'gallery_index_view.html',context)


# Render the Gallery page for a given profile:
def profile_gallery(request,profile_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    gallery_profile = Profile.objects.get(profile_id=profile_id)
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        colls = serialisers.serialise_community_per_profile_items(request,gallery_profile)    
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':gallery_profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'interaction_banner_name':'Gallery','collection_label_links':True}
        return render(request,'gallery_profile_index_view.html',context)


# Render the Gallery page for a given profile and collection:
def profile_gallery_collection(request,profile_id,collection_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    gallery_profile = Profile.objects.get(profile_id=profile_id)
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        collection = GalleryCollection.objects.get_or_create(collection_id=collection_id)[0]
        colls = serialisers.serialise_community_per_profile_items(request,gallery_profile,collection)    
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':gallery_profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'interaction_banner_name':'Gallery: '+collection.label,'collection_nav_links':True}
        return render(request,'gallery_profile_index_view.html',context)

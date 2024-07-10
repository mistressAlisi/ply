from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from communities.profiles.models import Profile
from media.gallery.core import serialisers
from media.gallery.core.models import GalleryCollection
from core.metrics.models import GalleryCollectionPageHit,GalleryProfilePageHit,GalleryHomePageHit
from core.metrics.toolkit import request_data_capture
# Render the Gallery Home page:
def gallery_home(request):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    sideBar = SideBarBuilder()
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    # Create the core metrics:
    gal_hit = GalleryHomePageHit.objects.create(type="GALPAGE",community=community)
    request_data_capture(request,gal_hit)        
        
    request.session['community'] = str(community.uuid)
    colls = serialisers.serialise_community_items(request)    
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}
    return render(request,'gallery_index_view.html',context)


# Render the Gallery page for a given profile:
def profile_gallery(request,profile_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    sideBar = SideBarBuilder()
    gallery_profile = get_object_or_404(Profile,profile_id=profile_id)
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    request.session["community"] = str(community.uuid)
    # Create the core metrics:
    gal_hit = GalleryProfilePageHit.objects.create(profile=gallery_profile,type="GALPAGE",community=community)
    request_data_capture(request,gal_hit)
    # Now render the page: 
    colls = serialisers.serialise_community_per_profile_items(request, gallery_profile)
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':gallery_profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL
               ,'interaction_banner_name':'Gallery','collection_label_links':True}
    return render(request,'gallery_profile_index_view.html',context)


# Render the Gallery page for a given profile and collection:
def profile_gallery_collection(request,profile_id,collection_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    sideBar = SideBarBuilder()
    gallery_profile = get_object_or_404(Profile,profile_id=profile_id)
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    request.session["community"] = str(community.uuid)
    #collection = GalleryCollection.objects.get(collection_id=collection_id)
    collection = get_object_or_404(GalleryCollection,collection_id=collection_id)
    # Create the core metrics:
    gal_hit = GalleryCollectionPageHit.objects.create(collection=collection,type="GALCOLPAGE",community=community)
    request_data_capture(request,gal_hit)
    # Now render the page: 
    colls = serialisers.serialise_community_per_profile_items(request, gallery_profile, collection)
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':gallery_profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'interaction_banner_name':'Gallery: '+collection.label,'collection_nav_links':True}
    return render(request,'gallery_profile_index_view.html',context)

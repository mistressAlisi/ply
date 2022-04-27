from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

import ply
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from gallery.models import GalleryItemsByCollectionPermission
from metrics.models import CommunityPageHit
from metrics.toolkit import request_data_capture
# Render the User Dashboard Home page:
def community_home(request):
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
        # Create the community metrics:
        gal_hit = CommunityPageHit.objects.create(community=community,type="COMPAGE")
        request_data_capture(request,gal_hit)
        # now render the page:
        if (community.backgroundItem is not False):
            try:
                bkg_item = GalleryItemsByCollectionPermission.objects.get(item=community.backgroundItem,gif_thumbnail=False)
                path = ply.toolkit.file_uploader.get_temp_path(bkg_item.file.name,bkg_item.profile)
                bkg_path = f"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{path}"
            except GalleryItemsByCollectionPermission.DoesNotExist:
                bkg_path= ""

        else:
            bkg_path = False
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,'ply_version':ply.settings.PLY_VERSION,'bkg_path':bkg_path}
        return render(request,community.dynapage.template.filename,context)


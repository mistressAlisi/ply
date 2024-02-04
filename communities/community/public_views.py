from django.shortcuts import render
# Create your views here.

import ply
from ply.toolkit import vhosts,profiles,themes,version
from dashboard.navigation import SideBarBuilder
from media.gallery.core.models import GalleryItemsByCollectionPermission
from core.metrics.models import CommunityPageHit
from core.metrics.toolkit import request_data_capture

# Render the User Dashboard Home page:
def community_home(request):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    request.session["community"] = str(community.uuid)

    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        theme = themes.get_community_theme_or_def(community)
        # Create the community metrics:
        gal_hit = CommunityPageHit.objects.create(community=community,type="COMPAGE")
        request_data_capture(request,gal_hit)
        # now render the page:

        if (community.backgroundItem is not False):
            try:
                bkg_item = GalleryItemsByCollectionPermission.objects.filter(item=community.backgroundItem,gif_thumbnail=False)
                path = ply.toolkit.file_uploader.get_temp_path(bkg_item[0].file.name,bkg_item[0].profile)
                bkg_path = f"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{path}"
            except GalleryItemsByCollectionPermission.DoesNotExist:
                bkg_path= ""
            except IndexError:
                bkg_path= ""
        else:
            bkg_path = ""
        vers = version.get_version_str
        context = {'community':community,'vhost':vhost,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,'ply_version':vers,'bkg_path':bkg_path,'THEME_PATH':theme.THEME_PATH}
        return render(request,"dynapages/"+community.dynapage.template.filename,context)


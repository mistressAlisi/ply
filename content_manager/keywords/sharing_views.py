from django.shortcuts import render
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts,profiles
from content_manager.keywords.models import Keyword


# Render the core Share card/page:
def keyword_share_search_view(request,keyword_search):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session["community"] = str(community.uuid)
        try:
            keyword = Keyword.objects.get(hash=keyword_search)
        except Keyword.DoesNotExist:
            return render(request,"error-404-not-found.html",{})
        if request.user.is_authenticated:
            profile = profiles.get_active_profile(request)
            all_profiles = profiles.get_all_profiles(request)
        else:
            profile = False
            all_profiles = False

        base_url = ply.settings.PLY_GALLERY_SHARE_URL_BASE_URL+"/"
        context = {'community':community,'vhost':vhost,'profile':profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,'keyword':keyword,"base_url":base_url,'ua':request.headers["User-Agent"],'keyword_search':keyword_search}
        return render(request,'keywords/share_search_view.html',context)


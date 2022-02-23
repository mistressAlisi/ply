from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

import ply
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
# Render the User Dashboard Home page:
def community_home(request):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
    else:
        profile = False
    #all_profiles = profiles.get_all_profiles(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,community.dynapage.template.filename,context)


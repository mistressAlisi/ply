from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
# Create your views here.

# Render the User Dashboard Home page:
@login_required
def dashboard_home(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':profile,'profiles':all_profiles}
        return render(request,"dashboard.html",context)

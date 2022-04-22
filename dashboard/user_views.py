from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile

# Render the User Dashboard Home page:
@login_required
def dashboard_home(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,'profiles':all_profiles,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path}
        return render(request,"dashboard.html",context)


@login_required
def dashboard_profile_switch(request,puuid):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    sideBar = SideBarBuilder()
    profile = profiles.get_profile(request,puuid)
    if 'r' in request.GET:
        ret = request.GET['r']
        if (ret != ""):
            return redirect(ret)
        else:
            return redirect("/dashboard/user")
    else:
        return redirect("/dashboard/user/")

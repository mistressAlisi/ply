from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles,dynapages as dp_tools
from dashboard.navigation import SideBarBuilder
from communities.community.models import CommunityAdmins
from communities.group.models import GroupMember
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience
# Render the User Dashboard Home page:
@login_required
def dashboard_home(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = (vhosts.get_vhost_community(hostname=vhost))

    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    sideBar = SideBarBuilder(settings.PLY_WORLDFORGE_DASHBOARD_MODULES, "sidebar_forge")
    context = {'community':community,'vhost':vhost,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'ply_version':settings.PLY_VERSION,'sidebar':sideBar.modules.values()}
    return render(request,'dashboard/community_admin/dashboard/index.html',context)


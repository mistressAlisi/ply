from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from almanac.models import AlmanacMenuCategory,AlmanacMenuCategoryEntry,AlmanacPage,AlmanacPageText
from community.models import CommunityAdmins
# Render the User Dashboard Home page:
@login_required
def almanac_home(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    
    #Almanac menu builder:
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)

    if (len(is_admin) == 0):
        enable_admin = False
    else:
        enable_admin = True
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'enable_admin':enable_admin,'url_path':request.path}
        return render(request,"almanac_dashboard.html",context)


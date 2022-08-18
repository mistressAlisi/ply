from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from group.models import Group,GroupMember,GroupTitle
from stats.models import BaseStat,ProfileStat
from dynapages import models as dynapages
from profiles.models import ProfilePageNode
from stats.models import BaseStat,ProfileStat
# Render the User Dashboard Home page:
@login_required
def dashboard_home(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    try:
        groups = GroupMember.objects.get(profile=request.session["profile"])
        primaryGroup = GroupMember.objects.get(profile=request.session["profile"],primary=True)
    except GroupMember.DoesNotExist:
        groups = []
        primaryGroup = False
    profilePage = ProfilePageNode.objects.get(profile=profile,node_type='dashboard')
    widgets = dynapages.PageWidget.objects.order_by('order').filter(page=profilePage.dynapage)
    stats = ProfileStat.objects.filter(profile=profile)
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,'profiles':all_profiles,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,'ply_version':settings.PLY_VERSION,'widgets':widgets,'template':profilePage.dynapage.template.filename,'dynapage_page_name':f"@{profile.profile_id}'s Dashboard",'profile':profile,"stats":stats}
    return render(request,'profile_dashboard_dynapage_wrapper.html',context)


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




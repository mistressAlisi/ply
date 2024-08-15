from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from communities.preferences.models import Preferences
# Create your views here.
# PLY:
from ply import settings
from ply.toolkit import vhosts, profiles, contexts, version, dynapages as dp_tools, themes
from dashboard.navigation import SideBarBuilder, SideBarBuilder_dynamic
from communities.group.models import GroupMember
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from communities.community.models import CommunityProfileDashboardRoles
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience

import logging

log = logging.getLogger(__name__)


# Render the User Dashboard Home page:
@login_required
def dashboard_home(request):

    context, vhost, community, profile = contexts.default_context(request)
    # vhost,community,context = request.META["HTTP_HOST"].split(":")[0]
    # community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request, "error-no_vhost_configured.html", {})
    else:
        request.session["community"] = str(community.uuid)
    # This is a rare condition, but in early-stage databases, an admin user may be using the default system profile. If this condition arises; we re-direct the user to /select_profile where they can either select a proper profile, or
    # go through the forge process to create a new, non-system profile.
    if profile.system is True:
        return redirect("/forge/select/profile/")
    all_profiles = profiles.get_all_profiles(request)
    sideBar = SideBarBuilder_dynamic(community=community, application_mode="user")
    sidebar_modules = sideBar.get_dynamic_sidebar(community,"user")
    profile = profiles.get_active_profile(request)
    try:
        groups = GroupMember.objects.get(profile=request.session["profile"])
        primaryGroup = GroupMember.objects.get(
            profile=request.session["profile"], primary=True
        )
    except GroupMember.DoesNotExist:
        groups = []
        primaryGroup = False
    # profilePage = ProfilePageNode.objects.get(profile=profile,node_type='dashboard')
    log.error(f"Profile Dashboard Home, f{profile}")
    profilePage = ProfilePageNode.objects.get(profile=profile, node_type="dashboard")
    # Don't allow empty profile Page nodes.
    # This check will automatically fix the condition if it ever arises:
    if profilePage.dynapage == None:
        log.info(f"Initialising Dynapages for {profile.profile_id}'s dashboard.")
        profilePage = dp_tools.dashboard_initDynaPage(request.user, profile)
    log.info(f"Profile Node: {profilePage.dynapage.pk}, {profilePage.node_type}")
    try:
        exo = ProfileExperience.objects.get(community=community, profile=profile)
    except:
        exo = {}

    widgets = dynapages.PageWidget.objects.order_by("order").filter(
        page=profilePage.dynapage
    )
    prefs = Preferences.objects.get_or_create(user=request.user)[0]

    stats = ProfileStat.objects.filter(profile=profile, community=community)
    dashboards = CommunityProfileDashboardRoles.objects.filter(
        profile=profile, community=community
    )
    if len(dashboards) > 0:
        show_dbswitch = True
    else:
        show_dbswitch = False
    theme = themes.get_community_theme_or_def(community)
    context.update(
        {
            "sidebar": sidebar_modules.values(),
            "current_profile": profile,
            "profiles": all_profiles,
            "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
            "url_path": request.path,
            "widgets": widgets,
            "template": profilePage.dynapage.template.filename,
            "dynapage_page_name": f"@{profile.profile_id}'s Dashboard",
            "profile": profile,
            "stats": stats,
            "profile_xp": exo,
            "show_dbswitch": show_dbswitch,
            "preferences":prefs,
            'THEME_PATH': theme.THEME_PATH

        }
    )
    return render(
        request, "communities_profiles/profile_dashboard_dynapage_wrapper.html", context
    )


@login_required
def dashboard_profile_switch(request, puuid):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = vhosts.get_vhost_community(hostname=vhost)
    profile = profiles.get_profile(request, puuid)
    if "r" in request.GET:
        ret = request.GET["r"]
        if ret != "":
            return redirect(ret)
        else:
            return redirect("/dashboard/user")
    else:
        return redirect("/dashboard/user/")

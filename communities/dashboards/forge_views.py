from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from ply.toolkit import vhosts, profiles
from communities.community.models import (
    Friend_ExpLvl_View,
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    CommunityRegistryPageView,
)
from communities.profiles.models import Profile
from ply.toolkit.contexts import default_context


# Create your views here.
def dashboard_studio(request):
    context, vhost, community, profile = default_context(request)
    context["dashboard_modes"] = CommunityRegistryPageView.objects.filter(
        community=community,
        grouping_key="community_appmode_dashboards"
    )
    return render(request, "communities.dashboards/studio/index.html", context)

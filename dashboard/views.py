from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles,contexts,dynapages as dp_tools
from dashboard.navigation import SideBarBuilder,SideBarBuilder_dynamic
from communities.community.models import CommunityDashboardType,CommunityProfileDashboardRoles
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience

import logging
log = logging.getLogger(__name__)
@login_required
def dashboard_selector(request):
    context,vhost,website,profile = contexts.default_context(request)
    dashboard_types = CommunityDashboardType.objects.filter(privileged=False)
    privileged_dashboard_types = CommunityProfileDashboardRoles.objects.filter(community=context['community']).distinct()
    context["dashboards"] = dashboard_types
    context["priv_dashboards"] = privileged_dashboard_types
    return render(request,"dashboard/selector/index.html",context)
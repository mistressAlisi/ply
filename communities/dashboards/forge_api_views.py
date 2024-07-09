from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import ply
from ply.toolkit import vhosts, profiles
from communities.community.models import (
    Friend_ExpLvl_View,
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    CommunityRegistryPageView,
)
from communities.profiles.models import Profile
from ply.toolkit.contexts import default_context, admin_context
from core.dynapages.models import Page, PageWidget,Widget
from ply.toolkit.dynapages import get_or_create_dynapage_node


# Create your views here.
@login_required
def load_dashboard(request, dashboard):
    context, vhost, community, profile = admin_context(request)
    dynapage = Page.objects.get(pk=dashboard)
    widgets = PageWidget.objects.filter(page=dynapage)
    context.update(
        {
            "dynapage": dynapage,
            "widgets": widgets,
        }
    )
    return render(
        request, "communities.dashboards/studio/render_dashboard.html", context
    )


def load_widgets_url(request, dashboard):
    dynapage = Page.objects.get(pk=dashboard)
    filters = {}
    if dynapage.system == True:
        filters["system"] = True
    if dynapage.profile_page == True:
        filters["profile"] = True
        filters["system"] = False
    if dynapage.widget_mode != False:
        filters[f"{dynapage.widget_mode}"] = True
    filter_q = Q(**filters)
    aw = Widget.objects.filter(active=True).filter(filter_q)
    available_widgets = serializers.serialize("json",aw)
    return JsonResponse({"res": "ok","widgets":available_widgets})

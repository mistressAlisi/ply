import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# PLY:
from ply import settings
from ply.toolkit import vhosts, profiles, contexts, dynapages as dp_tools
from dashboard.navigation import SideBarBuilder_dynamic
from communities.community.models import (
    CommunityAdmins,
    CommunityProfileDashboardRoles,
    CommunityStaff,
    CommunityDashboardType,
    CommunitySidebarMenu,
)
from communities.community.forms import (
    CommunityStaffForm,
    CommunityAdminForm,
    CommunitySidebarMenuForm,
)
from communities.group.models import GroupMember
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from ply.toolkit.core import get_ply_appinfo
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience


# Render the User Dashboard Home page:
@login_required
def create_community_staff(request):
    #  Ignore port:
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    form = CommunityStaffForm(request.POST)
    form.set_community(community)
    if not form.is_valid():
        return JsonResponse({"res": "err", "e": form.errors}, safe=False)
    else:
        form.save()
        dbt = CommunityDashboardType.objects.get(type="staff")
        db = CommunityProfileDashboardRoles.objects.get_or_create(
            profile=form.instance.profile, type=dbt, community=form.instance.community
        )[0]
        db.save()
        return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)


@login_required
def delete_community_staff(request, staff):
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    staffobj = CommunityStaff.objects.get(uuid=staff)
    dbt = CommunityDashboardType.objects.get(type="staff")
    dashobj = CommunityProfileDashboardRoles.objects.get(
        profile=staffobj.profile, community=staffobj.community, type=dbt
    )
    dashobj.delete()
    staffobj.delete()
    return JsonResponse({"res": "ok"}, safe=False)


@login_required
def create_community_admin(request):
    #  Ignore port:
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    form = CommunityAdminForm(request.POST)
    form.set_community(community)
    if not form.is_valid():
        return JsonResponse({"res": "err", "e": form.errors}, safe=False)
    else:
        form.save()
        return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)


@login_required
def delete_community_admin(request, staff):
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    staffobj = CommunityAdmins.objects.get(uuid=staff)
    staffobj.delete()
    return JsonResponse({"res": "ok"}, safe=False)


@login_required
def create_community_sidebar_menu(request):
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    if request.POST["not_edited"] == "False":
        form = CommunitySidebarMenuForm(request.POST, initial={"community": community})
        form.set_community(community)
        form.instance.not_edited = True
    else:
        instance = CommunitySidebarMenu.objects.get(pk=request.POST["uuid"])
        form = CommunitySidebarMenuForm(request.POST, instance=instance)
    if not form.is_valid():
        return JsonResponse({"res": "err", "e": form.errors}, safe=False)
    else:
        form.save()
        return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)


@login_required
def get_community_sidebar_menu(request, menu):
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    instance = CommunitySidebarMenu.objects.get(pk=menu)
    context["menu_form"] = CommunitySidebarMenuForm(instance=instance)
    return render(request, "dashboard/community_admin/menus/create_modal.html", context)


@login_required
def del_community_sidebar_menu(request, menu):
    context, vhost, community, profile = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    instance = CommunitySidebarMenu.objects.get(pk=menu)
    instance.delete()
    return JsonResponse({"res": "ok"}, safe=False)

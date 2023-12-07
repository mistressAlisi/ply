import uuid

from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles,contexts,dynapages as dp_tools
from dashboard.navigation import SideBarBuilder_dynamic
from communities.community.models import CommunityAdmins,CommunityProfileDashboardRoles,CommunityStaff,CommunityDashboardType
from communities.community.forms import CommunityStaffForm
from communities.group.models import GroupMember
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience
# Render the User Dashboard Home page:
@login_required
def create_community_staff(request):
    #  Ignore port:
    vhost,community,context = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    form = CommunityStaffForm(request.POST)
    form.set_community(community)
    if not form.is_valid():
        return JsonResponse({"res": "err", "e": form.errors}, safe=False)
    else:
        form.save()
        dbt = CommunityDashboardType.objects.get(type='staff')
        db = CommunityProfileDashboardRoles.objects.get_or_create(profile=form.instance.profile,type=dbt,community=form.instance.community)[0]
        db.save()
        return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)



@login_required
def delete_community_staff(request,staff):
    vhost,community,context = contexts.default_context(request)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    staffobj = CommunityStaff.objects.get(uuid=staff)
    dbt = CommunityDashboardType.objects.get(type='staff')
    dashobj = CommunityProfileDashboardRoles.objects.get(profile=staffobj.profile, community=staffobj.community,type=dbt)
    dashobj.delete()
    staffobj.delete()
    return JsonResponse({"res": "ok"}, safe=False)
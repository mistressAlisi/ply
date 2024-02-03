from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles,contexts,dynapages as dp_tools
from dashboard.navigation import SideBarBuilder_dynamic
from communities.community.models import CommunityAdmins,CommunityStaff
from communities.community.forms import CommunityStaffForm,CommunityAdminForm
from communities.group.models import GroupMember
from core.dynapages import models as dynapages
from communities.profiles.models import ProfilePageNode
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience
# Render the User Dashboard Home page:
@login_required
def community_staff(request):
    #  Ignore port:
    context,vhost,community,profile = contexts.default_context(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    staff = CommunityStaff.objects.filter(community=community)
    form = CommunityStaffForm()
    form.set_community(community)
    context["staff"] = staff
    context["staff_form"] = form
    return render(request,'dashboard/community_admin/community_staff/index.html',context)

@login_required
def community_admins(request):
    #  Ignore port:
    context,vhost,community,profile = contexts.default_context(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    staff = CommunityAdmins.objects.filter(community=community)
    form = CommunityAdminForm()
    form.set_community(community)
    context["admins"] = staff
    context["admin_form"] = form
    return render(request,'dashboard/community_admin/community_admins/index.html',context)



@login_required
def default_profile_editor(request):
    context,vhost,community,profile = contexts.default_context(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    try:
        groups = GroupMember.objects.get(profile=request.session["profile"])
        primaryGroup = GroupMember.objects.get(profile=request.session["profile"],primary=True)
    except GroupMember.DoesNotExist:
        groups = []
        primaryGroup = False
    profilePage = ProfilePageNode.objects.get(profile=profile,node_type='profile')
    print(f"Profile Node: {profilePage.dynapage.pk}, {profilePage.node_type}")
    widgets = dynapages.PageWidget.objects.order_by('order').filter(page=profilePage.dynapage)
    available_widgets = dynapages.Widget.objects.filter(active=True,profile=True)
    print(available_widgets)

    exp = ProfileExperience.objects.get(community=community,profile=profile)
    stats = ProfileStat.objects.filter(profile=profile)
    context = {'community':community,'vhost':vhost,'profile':profile,'widgets':widgets,'groups':groups,'primaryGroup':primaryGroup,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"stats":stats,'dynapage_template':profilePage.dynapage.template.filename,'dynapage_page_name':f"Default Community Profile",'available_widgets':available_widgets,'exp':exp}
    return render(request,'dynapages_tools/widget_editor.html',context)
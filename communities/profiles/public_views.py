from django.shortcuts import render,get_object_or_404

#PLY:
import ply
from core.dynapages import models as dynapages
from ply.toolkit import vhosts,profiles,contexts,themes
from communities.profiles.models import Profile,ProfilePageNode
from communities.group.models import GroupMember
from roleplaying.stats.models import ProfileStat
from communities.community.models import ProfilePerCoummunityView
from core.metrics.models import ProfilePageHit,ProfileIndexPageHit
from core.metrics.toolkit import request_data_capture
# Create your views here.

# Render the User Dashboard Home page:
def profile_view(request,profile_id):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = get_object_or_404(Profile,profile_id=profile_id)
    if request.user.is_authenticated:
        current_profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    try:
        groups = GroupMember.objects.get(profile=profile)
        primaryGroup = GroupMember.objects.get(profile=profile,primary=True)
    except GroupMember.DoesNotExist:
        groups = []
        primaryGroup = False
    # Create the Profile metrics:
    gal_hit = ProfilePageHit.objects.create(profile=profile,type="PROFILE",community=community)
    request_data_capture(request,gal_hit)
    # We need the profile template:
    profilePage = ProfilePageNode.objects.get(profile=profile,node_type='profile')
    print(f"Profile Node: {profilePage.dynapage.pk}, {profilePage.node_type}")
    # now render the page:
    widgets = dynapages.PageWidget.objects.order_by('order').filter(page=profilePage.dynapage)
    stats = ProfileStat.objects.filter(profile=profile)

    context = {'community':community,'vhost':vhost,'profile':profile,'widgets':widgets,'groups':groups,'primaryGroup':primaryGroup,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,"stats":stats,'template':profilePage.dynapage.template.filename,'current_profile':current_profile,'profiles':all_profiles}
    return render(request,'communities_profiles/profile_dashboard_dynapage_wrapper.html',context)

# Render the User Profile Directory (index) for this community:
def profile_index(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    view_profiles = ProfilePerCoummunityView.objects.filter(community=community).order_by('profile_created')
    if request.user.is_authenticated:
        current_profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        current_profile = False
        all_profiles = []
    # Create the Profile metrics:
    gal_hit = ProfileIndexPageHit.objects.create(type="PROFILEINX",community=community)
    request_data_capture(request,gal_hit)
    context = {'community':community,'vhost':vhost,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'current_profile':current_profile,'profiles':all_profiles,'all_profiles':view_profiles}
    return render(request,'profiles_index_view.html',context)

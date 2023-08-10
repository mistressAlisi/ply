from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#PLY:
from core.dynapages import models as dynapages
import ply
from ply.toolkit import vhosts
from communities.profiles.models import Profile,ProfilePageNode
from communities.group.models import GroupMember
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience


# Create your views here.

# Render the User Dashboard Home page:
@login_required
def profile_view(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = Profile.objects.get(uuid=request.session["profile"])
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
    exp = ProfileExperience.objects.get(community=community,profile=profile)
    stats = ProfileStat.objects.filter(profile=profile)
    context = {'community':community,'vhost':vhost,'profile':profile,'widgets':widgets,'groups':groups,'primaryGroup':primaryGroup,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,"stats":stats,'dynapage_template':profilePage.dynapage.template.filename,'dynapage_page_name':f"@{profile.profile_id}'s profile",'available_widgets':available_widgets,'exp':exp}
    return render(request,'dynapages_tools/widget_editor.html',context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from communities.stream.forge_forms import XMPPSettingsForm
from communities.stream.models import StreamXMPPSettings
from ply.toolkit import vhosts,profiles,contexts
from communities.community.models import CommunityAdmins
from communities.profiles.models import Profile


# Create your views here.
@login_required
def configure_xmpp(request):
    context,vhost,community,profile = contexts.admin_context(request)
    settings = StreamXMPPSettings.objects.get_or_create(community=community)[0]
    xmpp_form = XMPPSettingsForm(initial={'community':community},instance=settings)
    context["form"] = xmpp_form
    return render(request,"communities.stream/forge/config/xmpp.html",context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from communities.stream.forge_forms import XMPPSettingsForm
from ply.toolkit import vhosts,profiles,contexts
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile


# Create your views here.
@login_required
def configure_xmpp(request):
    vhost,community,context = contexts.default_context(request)
    xmpp_form = XMPPSettingsForm()
    context["form"] = xmpp_form
    return render(request,"communities.stream/forge/config/xmpp.html",context)

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from communities.stream.forge_forms import XMPPSettingsForm
from communities.stream.models import StreamXMPPSettings
from ply.toolkit import vhosts, profiles, contexts
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile


# Create your views here.
@login_required
def config_xmpp(request):
    context,vhost,community,profile = contexts.admin_context(request)
    settings = StreamXMPPSettings.objects.get_or_create(community=community)[0]
    xmpp_form = XMPPSettingsForm(request.POST,instance=settings)
    if (xmpp_form.is_valid()):
        xmpp_form.instance.save()
    else:
        return JsonResponse({"res": "err", "e": xmpp_form.errors}, safe=False)
    return JsonResponse({"res":"ok"},safe=False)


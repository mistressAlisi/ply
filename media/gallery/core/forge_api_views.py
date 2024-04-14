import importlib

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from media.gallery.core.forge_forms import CoreSettingsForm
from media.gallery.core.models import GalleryCoreSettings
from ply.toolkit import vhosts,profiles
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile
from ply.toolkit.contexts import default_context


# Create your views here.

def settings_save(request):
    context,vhost,community,profile = default_context(request)
    core_settings_obj = GalleryCoreSettings.objects.get_or_create(community=community)[0]
    form = CoreSettingsForm(request.POST,instance=core_settings_obj)
    if not form.is_valid():
        return JsonResponse({"res": "err", "e": form.errors}, safe=False)
    else:
        form.save()
        core_settings_obj.save()
        return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)





def plugin_settings_save(request):
    context, vhost, community, profile = default_context(request)
    plugin = request.POST["plugin"]
    try:
        forge_form = importlib.import_module(f"{plugin}.forge_forms")
        instance = (forge_form.Forge_Form.Meta.model.objects.get(community=community))
        form = forge_form.Forge_Form(request.POST,instance=instance)
        if not form.is_valid():
            return JsonResponse({"res": "err", "e": form.errors}, safe=False)
        else:
            form.save()
            instance.save()
            return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)
    except ModuleNotFoundError:
        return JsonResponse({"res": "err", "e": "Module does not have a forge_forms class."}, safe=False)

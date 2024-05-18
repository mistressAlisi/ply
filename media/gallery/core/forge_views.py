import importlib

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from media.gallery.core.forge_forms import CoreSettingsForm
from media.gallery.core.models import GalleryCoreSettings, GalleryPlugins
from ply.toolkit import vhosts, profiles
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile
from ply.toolkit.contexts import default_context

# from ufls.registrar.forms import NewLevelForm, AddLootForm, CreateLootForm
# from ufls.registrar.models import RegistrantLevel


# Create your views here.
@login_required
def setup(request):
    context, vhost, community, profile = default_context(request)
    core_settings_obj = GalleryCoreSettings.objects.get_or_create(community=community)[
        0
    ]
    context["gallery_form"] = CoreSettingsForm(instance=core_settings_obj)
    # new_level_form = NewLevelForm()
    # add_loot_form = AddLootForm()
    # create_loot_form = CreateLootForm()
    # context["new_level_form"] = new_level_form
    # context["add_loot_form"] = add_loot_form
    # context["create_loot_form"] = create_loot_form
    # context["levels"] = RegistrantLevel.objects.all()
    return render(request, "media.gallery.core/world_forge/setup.html", context)


def plugin_setup(request, plugin):
    context, vhost, community, profile = default_context(request)
    plugin_data = GalleryPlugins.objects.get(app=plugin)
    context["plugin"] = plugin_data
    try:
        forge_form = importlib.import_module(f"{plugin}.forge_forms")
        instance = forge_form.Forge_Form.Meta.model.objects.get_or_create(community=community)[0]
        context["setup_form"] = forge_form.Forge_Form(instance=instance)
        return render(request, "media.gallery.core/world_forge/plugin_setup.html", context)
    except ModuleNotFoundError:
        return render(request, "media.gallery.core/world_forge/no_plugin_setup.html", context)
    return JsonResponse({"res": "ok", "pk": plugin}, safe=False)

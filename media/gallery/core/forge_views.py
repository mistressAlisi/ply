from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from ply.toolkit import vhosts,profiles
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile
from ply.toolkit.contexts import default_context
from ufls.registrar.forms import NewLevelForm, AddLootForm, CreateLootForm
from ufls.registrar.models import RegistrantLevel


# Create your views here.
@login_required
def setup(request):
    context,vhost,community,profile = default_context(request)
    # new_level_form = NewLevelForm()
    # add_loot_form = AddLootForm()
    # create_loot_form = CreateLootForm()
    # context["new_level_form"] = new_level_form
    # context["add_loot_form"] = add_loot_form
    # context["create_loot_form"] = create_loot_form
    # context["levels"] = RegistrantLevel.objects.all()
    return render(request,"media.gallery.core/world_forge/setup.html",context)


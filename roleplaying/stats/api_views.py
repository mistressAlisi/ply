from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ply.toolkit import vhosts,profiles,stats
from django.http import JsonResponse
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience
from roleplaying.stats.forms import AssignStatForm

# Create your views here.

# Save a script from scriptStudio:
@login_required
@transaction.atomic
# Assign stats to a profile:
def assign_to_profile(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    exp = ProfileExperience.objects.get(community=community,profile=profile)
    form_saver = AssignStatForm(request.POST,profile=profile,community=community,exp=exp)
    if (not form_saver.is_valid()):
        return JsonResponse({"res":"err","e":str(form_saver.errors.as_data())},safe=False)
    try:
        stat = ProfileStat.objects.get(uuid=form_saver.cleaned_data['stat'])
    except:
        return JsonResponse({"res":"err","e":"Invalid Stat selected!"},safe=False)
    if ((form_saver.cleaned_data["increase"] > exp.statpoints) or (form_saver.cleaned_data["increase"]+stat.value > stat.stat.maximum)):
        return JsonResponse({"res":"err","e":"I'm sorry dave, I can't let you do that."},safe=False)
    assign = stats.assign_stat(profile,community,stat,form_saver.cleaned_data["increase"])
    if assign == -1:
        return JsonResponse({"res":"err","e":"I'm sorry dave, I can't let you do that."},safe=False)
    elif assign is True:
        return JsonResponse("ok",safe=False)
    else:
        return JsonResponse({"res":"err","e":"Invalid Stat selected!"},safe=False)



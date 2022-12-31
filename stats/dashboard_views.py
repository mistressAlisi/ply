import ply
from ply import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from profiles.models import Profile
from django.http import JsonResponse,HttpResponse
from stats.models import ClassType,ProfileStat
from exp.models import ProfileExperience,ProfileExperienceHistory
from stats.forms import AssignStatForm
# Create your views here.

# Render the User Dashboard Home page:
@login_required
def all_stats(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    exp = ProfileExperience.objects.get(community=community,profile=profile)
    pstats = ProfileStat.objects.filter(community=community,profile=profile)
    assign_form = AssignStatForm(profile=profile,community=community,exp=exp)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exp,"assign_form":assign_form,"stats":pstats}
    return render(request,"stats/all_stats.html",context)



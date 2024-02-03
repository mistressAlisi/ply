from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from roleplaying.stats.models import ProfileStat
from roleplaying.exp.models import ProfileExperience
from ply import settings
# Create your views here.

# Render the User Dashboard Home page:
@login_required
def all_skills(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    nlvl = exo.next_level()
    pstats = ProfileStat.objects.filter(community=community,profile=profile)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exo,"next":nlvl,"stats":pstats}
    return render(request,"skills/all_skills.html",context)



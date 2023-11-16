from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ply import settings,toolkit
from ply.toolkit import vhosts,levels,themes
from roleplaying.stats.models import ClassType,ProfileStat
from roleplaying.exp.models import ProfileExperience


# Create your views here.


# Render the Select Profile Forge Page:
@login_required
def select_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    theme = themes.get_community_theme_or_def(community)

    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        all_profiles = toolkit.profiles.get_all_profiles(request)
        if (all_profiles.count() == 0):
            return redirect("/forge/create/profile")
        request.session['community'] = str(community.uuid)
        print(settings.PLY_DEFAULT_THEME)
        context = {'community':community,'vhost':vhost,'THEME_PATH':theme.THEME_PATH,'profiles':all_profiles,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,"forge-select_profile.html",context)


# Render the Create Profile Forge Page:
@login_required
def create_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_placeholder_profile(request)
    classes = ClassType.objects.filter(selectable=True,frozen=False,archived=False,blocked=False)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profile':profile,'classtypes':classes,'class_skip':False}
        return render(request,"forge-create_profile.html",context)


# Render the Edit Profile Forge Page:
@login_required
def edit_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})

    else:
        # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
        profile = toolkit.profiles.get_active_profile(request)
        exo = ProfileExperience.objects.get(community=community,profile=profile)
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exo,'class_skip':True}
        return render(request,"forge-create_profile.html",context)




# Render the Create Profile Preview Forge Page:
@login_required
def create_profile_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_placeholder_profile(request)
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exo}
    return render(request,"forge-preview_profile.html",context)

# Render the Edit Profile Preview Forge Page:
@login_required
def edit_profile_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_active_profile(request)
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exo}
    return render(request,"forge-preview_profile.html",context)




@login_required
@transaction.atomic
def level_up(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_active_profile(request)
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    nlvl = exo.next_level()
    pstats = ProfileStat.objects.filter(community=community,profile=profile)
    request.session['community'] = str(community.uuid)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,"exp":exo,"next":nlvl,"stats":pstats}
    if (levels.can_levelup(profile,community) is True):
        # Level up time!
        context["exp"] = levels.levelup(profile,community)
        return render(request,"forge/levelup/levelup.html",context)
    else:
        return render(request,"forge/levelup/no_levelup.html",context)

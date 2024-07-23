from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply import settings
from ply.toolkit import vhosts, profiles, version
from communities.community.models import CommunityAdmins
from media.gallery.core.models import GalleryItem
from core.dynapages import models as dynaModels
from core.forge.forms import NewScriptForm, SaveScriptForm
from media.gallery.core.forge_forms import CoreSettingsForm
from ply.toolkit.themes import get_installed_themes


# Create your views here.


# Render the Edit Community Cover Forge Page:
@login_required
def edit_community_cover(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = vhosts.get_vhost_community(hostname=vhost)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    templates = dynaModels.Templates.objects.filter(
        page_template=True, archived=False, blocked=False
    )
    backgroundItems = GalleryItem.objects.filter(profile=profile, active=True)
    themes = get_installed_themes()
    print(themes)
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    if community is None:
        return render(request, "error-no_vhost_configured.html", {})
    else:
        request.session["community"] = str(community.uuid)
        context = {
            "community": community,
            "vhost": vhost,
            "profile": profile,
            "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
            "hostname": settings.PLY_HOSTNAME,
            "editing_mode": True,
            "templates": templates,
            "backgroundItems": backgroundItems,
            "themes":themes
        }
        return render(request, "forge-create_community.html", context)


@login_required
def edit_community_cover_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = vhosts.get_vhost_community(hostname=vhost)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    templates = dynaModels.Templates.objects.filter(
        page_template=True, archived=False, blocked=False
    )
    backgroundItems = GalleryItem.objects.filter(profile=profile, active=True)
    all_profiles = profiles.get_all_profiles(request)
    vers = version.get_version_str
    context = {
        "community": community,
        "vhost": vhost,
        "profile": profile,
        "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
        "editing_mode": True,
        "templates": templates,
        "backgroundItems": backgroundItems,
        "enable_admin": True,
        "current_profile": profile,
        "profiles": all_profiles,
        "ply_version": vers(),
    }
    return render(request, "forge-preview_community.html", context)


@login_required
def script_studio(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = vhosts.get_vhost_community(hostname=vhost)
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(
        community=community, profile=profile, active=True
    )
    if len(is_admin) < 1:
        return render(request, "error-access-denied.html", {})
    templates = dynaModels.Templates.objects.filter(
        page_template=True, archived=False, blocked=False
    )
    backgroundItems = GalleryItem.objects.filter(profile=profile, active=True)
    all_profiles = profiles.get_all_profiles(request, True)
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    if community is None:
        return render(request, "error-no_vhost_configured.html", {})
    else:
        request.session["community"] = str(community.uuid)
        nsf = NewScriptForm()
        ssf = SaveScriptForm()
        vers = version.get_version_str

        context = {
            "community": community,
            "vhost": vhost,
            "profile": profile,
            "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
            "hostname": settings.PLY_HOSTNAME,
            "editing_mode": True,
            "templates": templates,
            "backgroundItems": backgroundItems,
            "enable_admin": True,
            "current_profile": profile,
            "profiles": all_profiles,
            "ply_version": vers.get_version_str(),
            "new_script_form": nsf,
            "save_script_form": ssf,
        }
        return render(request, "forge/script_studio/embedded.html", context)

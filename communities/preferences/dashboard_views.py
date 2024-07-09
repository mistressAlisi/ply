from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# PLY:
from ply import settings
from ply.toolkit import vhosts, profiles, version
from dashboard.navigation import SideBarBuilder
from communities.preferences.models import Preferences
from communities.preferences.forms import PreferencesForm


# Render the User Dashboard Home page:
@login_required
def system_settings(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0]
    community = vhosts.get_vhost_community(hostname=vhost)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    if community is None:
        return render(request, "error-no_vhost_configured.html", {})
    else:
        request.session["community"] = str(community.uuid)
        upreference = Preferences.objects.get_or_create(user=request.user)[0]
        preferencesForm = PreferencesForm(instance=upreference)
        vers = version.get_version_str

        context = {
            "community": community,
            "vhost": vhost,
            "sidebar": sideBar.modules.values(),
            "current_profile": profile,
            "profiles": all_profiles,
            "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
            "url_path": request.path,
            "preferencesForm": preferencesForm,
            "ply_version": vers
        }
        return render(request, "preferences-system_settings.html", context)

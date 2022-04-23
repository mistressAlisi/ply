from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply import settings
from ply.toolkit import vhosts,profiles
from profiles.models import Profile
# Create your views here.

# Render the Create Profile Forge Page:
@login_required
def create_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = profiles.get_placeholder_profile(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profile':profile}
        return render(request,"forge-create_profile.html",context)


# Render the Edit Profile Forge Page:
@login_required
def edit_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = profiles.get_active_profile(request)
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,"forge-create_profile.html",context)




# Render the Create Profile Preview Forge Page:
@login_required
def create_profile_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = profiles.get_placeholder_profile(request)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"forge-preview_profile.html",context)

# Render the Edit Profile Preview Forge Page:
@login_required
def edit_profile_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = profiles.get_active_profile(request)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"forge-preview_profile.html",context)


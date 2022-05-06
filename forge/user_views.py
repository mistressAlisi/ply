from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ply import settings,toolkit
from ply.toolkit import vhosts
from profiles.models import Profile
# Create your views here.


# Render the Select Profile Forge Page:
@login_required
def select_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        all_profiles = toolkit.profiles.get_all_profiles(request)
        if (all_profiles.count() == 0):
            return redirect("/forge/create/profile")
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profiles':all_profiles,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,"forge-select_profile.html",context)


# Render the Create Profile Forge Page:
@login_required
def create_profile(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_placeholder_profile(request)
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
    profile = toolkit.profiles.get_active_profile(request)
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
    profile = toolkit.profiles.get_placeholder_profile(request)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"forge-preview_profile.html",context)

# Render the Edit Profile Preview Forge Page:
@login_required
def edit_profile_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    profile = toolkit.profiles.get_active_profile(request)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,"forge-preview_profile.html",context)


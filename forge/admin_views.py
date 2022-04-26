from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply import settings
from ply.toolkit import vhosts,profiles
from community.models import CommunityAdmins
from gallery.models import GalleryItem
from profiles.models import Profile
from dynapages import models as dynaModels
# Create your views here.


# Render the Edit Community Cover Forge Page:
@login_required
def edit_community_cover(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    templates = dynaModels.Templates.objects.filter(page_template=True,archived=False,blocked=False)
    backgroundItems = GalleryItem.objects.filter(profile=profile,active=True) 
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session['community'] = str(community.uuid)
        context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'hostname':settings.PLY_HOSTNAME,'editing_mode':True,'templates':templates,'backgroundItems':backgroundItems}
        return render(request,"forge-create_community.html",context)



@login_required
def edit_community_cover_preview(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = profiles.get_active_profile(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) < 1):
        return render(request,"error-access-denied.html",{})
    # The FORGE will create a new profile using this view. The first step is to get a placeholder profile so we can start assigning items and data to it:
    templates = dynaModels.Templates.objects.filter(page_template=True,archived=False,blocked=False)
    backgroundItems = GalleryItem.objects.filter(profile=profile,active=True) 
    print(request.POST)
    context = {'community':community,'vhost':vhost,'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'editing_mode':True,'templates':templates,'backgroundItems':backgroundItems}
    return render(request,"forge-preview_community.html",context)


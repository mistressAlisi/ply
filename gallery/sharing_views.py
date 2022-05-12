from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts,profiles,file_uploader
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from gallery import serialisers
from gallery.models import GalleryCollection,GalleryItem,GalleryItemsByCollectionPermission
from metrics.models import GalleryItemHit
from metrics.toolkit import request_data_capture

# Render the gallery Share card/page:
def gallery_item(request,profile_id,collection_id,item_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session["community"] = str(community.uuid)
        try:
            item = GalleryItemsByCollectionPermission.objects.filter(collection_id=collection_id,item_id=item_id,profile_slug=profile_id,gif_thumbnail=True).order_by('-gif_size')[0]
        except GalleryItemsByCollectionPermission.DoesNotExist:
            return render(request,"error-404-not-found.html",{})
        # Create the gallery metrics:
        gal_hit = GalleryItemHit.objects.create(type="SHAREOPEN",community=community,item=item.item)
        request_data_capture(request,item.item)
        base_url = ply.settings.PLY_GALLERY_SHARE_URL_BASE_URL+"/"+file_uploader.get_temp_path("",item.profile)
        context = {'community':community,'vhost':vhost,'url_path':request.path,'item':item,"base_url":base_url}
        return render(request,'gallery_sharing_card_link.html',context)

from django import template
from ply import toolkit
import ply
register = template.Library()

from media.gallery.core.models import GalleryItemsByCollectionPermission

@register.filter
def thumbnail_card(item):
    contents = GalleryItemsByCollectionPermission.objects.filter(gc_uuid=item.contents_json["col"],gci_uuid=item.contents_json["item"],gif_thumbnail=True).order_by('-gif_size')
    if (len(contents)>0):
        contents = contents[0]
        contents.item.views += 1
        contents.collection.views += 1
        contents.item.save()
        contents.collection.save()
        file_path = toolkit.file_uploader.get_temp_path("",contents.profile)
        card_str = f"<br/><div class=\"card\"><div class=\"card-header\"><span class=\"h5\"><a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\">\"{contents.gci_title}\"</a></span> in Collection <a href=\"/gallery/@{contents.profile.profile_id}/{contents.gc_id}\" target=\"_blank\">'<span class=\"h6\">{contents.gc_label}</span></a>':</div><div class=\"card-body\"><p><i class=\"fa-solid fa-eye\"></i>Views: {contents.gci_views}&#160;&#160;<i class=\"fa-solid fa-retweet\"></i> Reshares: {contents.gci_shares}&#160; <i class=\"fa-solid fa-heart\"></i>Favourites: {contents.gci_likes}</p><p>{contents.gci_descr}</p><p>By <a href=\"/profiles/@{contents.profile.profile_id}\" target=\"blank\"><img src=\"{ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}/{contents.profile.avatar}\" class=\"rounded-circle me-2 avatar img-fluid\" style=\"max-width: 45px; max-height: 45px;\"/>&#160;@{contents.profile.profile_id}</a></p><a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\"><img class=\"img-fluid\" src=\"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{file_path}{contents.gif_name}\"/></a></div><div class=\"card-footer\"></div></div>"
    else:
        card_str = f'<br><div class="alert alert-secondary" role="alert">This submission was deleted.</div>';
    return card_str

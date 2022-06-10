from django import template
from ply import toolkit
import ply
register = template.Library()

from gallery.models import GalleryCollection,GalleryItemsByCollectionPermission

@register.filter
def gallery_frame_widget(item):
    contents = GalleryItemsByCollectionPermission.objects.filter(gci_uuid=item.plugin_data["item"],gif_thumbnail=True).order_by('-gif_size')[0]
    contents.item.views += 1
    contents.collection.views += 1
    contents.item.save()
    contents.collection.save()
    file_path = toolkit.file_uploader.get_temp_path("",contents.profile)
    card_str = f"<br/><div class=\"card\"><div class=\"card-header\"><h5><i class=\"fa-solid fa-image\"></i>&#160;{item.plugin_data['title']}</h5></div><div class=\"card-body\"><a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\"><img class=\"img-fluid\" src=\"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{file_path}{contents.gif_name}\"/></a><br/><h6>\"{item.plugin_data['caption']}\"</h6><br/><p class=\"text-muted\"><i class=\"fa-solid fa-code-branch\"></i>Link to Original/share:&#160;<a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\">Original</a></p></div><div class=\"card-footer\"><i class=\"fa-solid fa-eye\"></i>Views: {contents.gci_views}&#160;&#160;<i class=\"fa-solid fa-retweet\"></i> Reshares: {contents.gci_shares}&#160; <i class=\"fa-solid fa-heart\"></i>Favourites: {contents.gci_likes}</div></div>"
    return card_str


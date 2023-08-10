from django import template
from ply import toolkit
import ply
register = template.Library()

from communities.stream.models import MessagesPerStreamView
from media.gallery.core.models import GalleryItemsByCollectionPermission
#from core.templatetags import thumbnail_card
@register.simple_tag
def stream_render_message(item, *args, **kwargs):
    if (item.message_type == "text/plain"):
        return f"<div class=\"card\"><div class=\"card-body\">{item.contents_text_parsed}</div><div class=\"card-footer\"><button type=\"button\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-retweet\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.reposts}</span></button>&#160;<button type=\"button\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-heart-circle-plus\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.likes}</span></button>&#160;<a href=\"/stream/@{item.author.profile_id}#msg-{item.message_uuid}\" target=\"_blank\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-share-nodes\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.shares}</span></a></div></div><br/>"
    elif (item.message_type == "application/ply.stream.refmsg"):
        if (item.stream_type == "PROFILE"):
            return f"<div class=\"card\"><div class=\"card-body\">{item.contents_text_parsed}</div><div class=\"card-footer\"><button type=\"button\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-retweet\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.reposts}</span></button>&#160;<button type=\"button\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-heart-circle-plus\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.likes}</span></button>&#160;<a href=\"/stream/@{item.author.profile_id}#msg-{item.message_uuid}\" target=\"_blank\" class=\"btn btn-light btn-outline-secondary text-muted\"><i class=\"fa-solid fa-share-nodes\"></i>&#160;<span class=\"badge rounded-pill text-muted\">{item.shares}</span></a></div></div><br/>"
    elif (item.message_type == "application/ply.stream.core"):
            contents = GalleryItemsByCollectionPermission.objects.filter(gc_uuid=item.contents_json["col"],gci_uuid=item.contents_json["item"],gif_thumbnail=True).order_by('-gif_size')
            if (len(contents)>0):
                contents = contents[0]
                contents.item.views += 1
                contents.collection.views += 1
                contents.item.save()
                contents.collection.save()
                file_path = toolkit.file_uploader.get_temp_path("",contents.profile)
                return f"<br/><div class=\"card\"><div class=\"card-header\"><span class=\"h5\"><a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\">\"{contents.gci_title}\"</a></span> in Collection <a href=\"/core/@{contents.profile.profile_id}/{contents.gc_id}\" target=\"_blank\">'<span class=\"h6\">{contents.gc_label}</span></a>':</div><div class=\"card-body\"><p><i class=\"fa-solid fa-eye\"></i>Views: {contents.gci_views}&#160;&#160;<i class=\"fa-solid fa-retweet\"></i> Reshares: {contents.gci_shares}&#160; <i class=\"fa-solid fa-heart\"></i>Favourites: {contents.gci_likes}</p><p>{contents.gci_descr}</p><p>By <a href=\"/profiles/@{contents.profile.profile_id}\" target=\"blank\"><img src=\"{ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}/{contents.profile.avatar}\" class=\"rounded-circle me-2 avatar img-fluid\" style=\"max-width: 45px; max-height: 45px;\"/>&#160;@{contents.profile.profile_id}</a></p><a href=\"/g/{contents.profile.profile_id}/{contents.gc_uuid}/{contents.gci_uuid}\" target=\"_blank\"><img class=\"img-fluid\" src=\"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{file_path}{contents.gif_name}\"/></a></div><div class=\"card-footer\"></div></div>"
            else:
                 return f'<br><div class="alert alert-secondary" role="alert">This submission was deleted.</div>';
    else:
        return ""




@register.simple_tag
def stream_casts_widget(item,profile, *args, **kwargs):
    count = item.plugin_data["count"]
    contents = MessagesPerStreamView.objects.filter(profile_uuid=profile.uuid).order_by('-message_created')[:count]
    contents_str = ""
    for msg in contents:
        contents_str += stream_render_message(msg)
    card_str = f"<br/><div class=\"card\"><div class=\"card-header\"><h5><i class=\"fa-solid fa-tower-broadcast\"></i>&#160;@{profile.profile_id}'s {count} latest casts:</h5></div><div class=\"card-body\">{contents_str}</div><div class=\"card-footer\"><a href=\"/stream/@{profile.profile_id}\" target=\"_blank\"><i class=\"fa-solid fa-share-from-square\"></i>&#160;Go to Stream!</a></div></div>"

    return card_str



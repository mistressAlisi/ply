from django import template

from communities.stream.templatetags.stream_casts_widget import stream_render_message
from ply import toolkit
import ply

register = template.Library()

from communities.stream.models import MessagesPerStreamView, MessagesPerNamedStreamView
from media.gallery.core.models import GalleryItemsByCollectionPermission


# from core.templatetags import thumbnail_card
@register.simple_tag
def stream_named_casts_widget(stream_name,count=5, *args, **kwargs):

    contents = MessagesPerNamedStreamView.objects.filter(
        stream_name=stream_name
    ).order_by("-message_created")[:count]
    contents_str = ""
    for msg in contents:
        contents_str += f'<br/><div class="card"><h5>@{msg.profile_id}\':</h5><div class="card-body">{msg.contents_text_parsed}</div>'

    return contents_str

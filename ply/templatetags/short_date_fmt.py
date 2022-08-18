from django import template
from ply import toolkit
from preferences.models import Preferences
import ply
register = template.Library()



@register.simple_tag
def short_date_fmt(date_obj, profile, *args, **kwargs):
    prefobj = Preferences.objects.get_or_create(profile=profile)[0]
    contents = DiceRoll.objects.filter(user=profile.creator).order_by('-date')[:count]
    contents_str = ""
    for msg in contents:
        contents_str += plydice_render_roll(msg)
    card_str = f"<br/><div class=\"card\"><div class=\"card-header\"><h5><i class=\"fa-solid fa-dice-d20\"></i>&#160;@{profile.profile_id}'s {count} latest rolls:</h5></div><div class=\"card-body\">{contents_str}</div><div class=\"card-footer\"><a href=\"/dice/@{profile.profile_id}\" target=\"_blank\"><i class=\"fa-solid fa-share-from-square\"></i>&#160;Roll History</a></div></div>"

    return date_obj.strftime(prefobj.shortdate)



from django import template

register = template.Library()
from communities.preferences.models import Preferences
from roleplaying.plydice.models import DiceRoll
#from core.templatetags import thumbnail_card
@register.simple_tag
def _plydice_render_roll(item, prefobj, *args, **kwargs):
    rds = ""
    for d in item.contents_json["dice"]:
        rds += str(d)+","
    if item.threshold <= item.result:
        roll_res = "<strong class=\"text-success\"><i class=\"fa-solid fa-check\"></i> Succesful!</strong>"
    else:
        roll_res = "<strong class=\"text-danger\"><i class=\"fa-solid fa-xmark\"></i> Unsuccesful :(</strong>"
    return f"<div class=\"card\"><div class=\"card-body\"><h5>Rolled {item.count}d{item.sides} at {item.date.strftime(prefobj.longdate)} for a {item.result} total roll.</h5> <h6>Threshold was: {item.threshold} -   Outcome: {roll_res}</h6><h6>Individual Rolls: {rds[:-1]}</h6></div><div class=\"card-footer\"><span class=\"text-muted\">Logged Reason: {item.contents_json['reason']}</span><br/>Roll Type: {item.type}</div></div><br/>"





@register.simple_tag
def plyrolls_latestrolls_widget(item,profile, *args, **kwargs):
    count = item.plugin_data["count"]
    contents = DiceRoll.objects.filter(profile=profile).order_by('-date')[:count]
    prefobj = Preferences.objects.get_or_create(user=profile.creator)[0]
    contents_str = ""
    for msg in contents:
        contents_str += _plydice_render_roll(msg,prefobj)
    card_str = f"<br/><div class=\"card\"><div class=\"card-header\"><h5><i class=\"fa-solid fa-dice-d20\"></i>&#160;@{profile.profile_id}'s {count} latest rolls:</h5></div><div class=\"card-body\">{contents_str}</div><div class=\"card-footer\"><a href=\"/dice/@{profile.profile_id}\" target=\"_blank\"><i class=\"fa-solid fa-share-from-square\"></i>&#160;Roll History</a></div></div>"

    return card_str



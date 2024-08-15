from django import template
import uuid

register = template.Library()
from communities.preferences.models import Preferences
from roleplaying.plydice.models import DiceEvent,DiceEventRoll



@register.simple_tag
def stream_roll_widget(event,profile, *args, **kwargs):
    dEvent = DiceEvent.objects.get(uuid=uuid.UUID(event))
    dRoll = DiceEventRoll.objects.get(community=dEvent.community,event=dEvent)
    prefobj = Preferences.objects.get_or_create(user=profile.creator)[0]
    rstr = f"<h3><i class=\"fa-solid fa-dice-d20\">&#160;{dRoll.roll.count}d{dRoll.roll.sides} Roll!</i></h3>"
    rds = ""
    for d in dRoll.roll.contents_json["dice"]:
        rds += str(d)+","
    if dRoll.roll.threshold <= dRoll.roll.result:
        roll_res = "<strong class=\"text-success\"><i class=\"fa-solid fa-check\"></i> Succesful!</strong>"
    else:
        roll_res = "<strong class=\"text-danger\"><i class=\"fa-solid fa-xmark\"></i> Unsuccesful :(</strong>"
    rstr += f"<h5>Rolled {dRoll.roll.count}d{dRoll.roll.sides} at {dRoll.roll.date.strftime(prefobj.longdate)} for a {dRoll.roll.result} total roll.</h5> <h6>Threshold was: {dRoll.roll.threshold} -   Outcome: {roll_res}</h6><h6>Individual Rolls: {rds[:-1]}</h6></div><div class=\"card-footer\"><span class=\"text-muted\">Logged Reason: {dRoll.roll.contents_json['reason']}</span><br/>Roll Type: {dRoll.roll.type}<br/>"
    return rstr



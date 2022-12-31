from django import template
from ply import toolkit
from preferences.models import Preferences
import ply
from pytz import timezone
register = template.Library()



@register.simple_tag
def short_date_fmt(date_obj, profile, *args, **kwargs):
    prefobj = Preferences.objects.get_or_create(user=profile.creator)[0]
    return date_obj.astimezone(timezone(prefobj.timezone.timezone)).strftime(prefobj.shortdatetime)



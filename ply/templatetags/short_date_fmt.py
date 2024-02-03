from django import template
from communities.preferences.models import Preferences
from pytz import timezone
register = template.Library()



@register.simple_tag
def short_date_fmt(date_obj, profile, *args, **kwargs):
    prefobj = Preferences.objects.get_or_create(user=profile.creator)[0]
    return date_obj.astimezone(timezone(prefobj.timezone.timezone)).strftime(prefobj.shortdatetime)



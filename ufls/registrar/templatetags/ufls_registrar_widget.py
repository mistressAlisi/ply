from django import template
from django.template.loader import render_to_string
register = template.Library()
from ufls.registrar.models import Event,RegistrantData
@register.simple_tag
def ufls_registrar_widget(item,profile, *args, **kwargs):
    _ev = item.plugin_data["event"]
    event = Event.objects.get(pk=_ev)
    regData = RegistrantData.objects.filter(event=event,profile=profile)
    context = {'profile':profile,'event':event,'regData':regData}
    if len(regData) == 0:
        contents_str = render_to_string("registrar/widget/not_registered.html",context)
    else:
        contents_str = render_to_string("registrar/widget/registered.html",context)

    return contents_str



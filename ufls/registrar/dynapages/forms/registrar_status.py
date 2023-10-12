from django import forms
from ply.toolkit import profiles
from ufls.registrar.models import Event
class WidgetForm(forms.Form):
    profile = False
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
            self.profile = profiles.get_active_profile(request)
        super().__init__(*args, **kwargs)
        EV = []
        events = Event.objects.filter(active=True)
        for ev in events:
            EV.append((ev.pk, ev.name))
        self.fields['event'].choices = EV
    event = forms.ChoiceField(label='Event :',min_value=1,max_value=10,initial=5)

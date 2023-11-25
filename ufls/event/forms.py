from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField

from ufls.event.models import Event,EventCommunityMapping
from django import forms
from django.forms.widgets import SelectDateWidget,HiddenInput
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["uuid",
                  "name","eventAppCode","active","isSecAccessEnabled","startDate","endDate","regOpen","regClose","dealersOpen","dealersClose","aaOpen","aaClose","eventsOpen","eventsClose"]
        widgets = {
            "uuid": HiddenInput(),
            "startDate":SelectDateWidget(),
            "endDate": SelectDateWidget(),
            "regOpen": SelectDateWidget(),
            "regClose": SelectDateWidget(),
            "dealersOpen": SelectDateWidget(),
            "dealersClose": SelectDateWidget(),
            "aaOpen": SelectDateWidget(),
            "aaClose": SelectDateWidget(),
            "eventsOpen": SelectDateWidget(),
            "eventsClose": SelectDateWidget(),
                   }



class EventCommunityMappingForm(ModelForm):
    class Meta:
        model = EventCommunityMapping
        fields = ["uuid","community","event","active"]
        widgets = {
            "uuid":HiddenInput(),
            "community":HiddenInput()
                   }

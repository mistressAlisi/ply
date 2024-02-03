from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField

from communities.stream.models import StreamXMPPSettings
from django import forms
from django.forms.widgets import SelectDateWidget,HiddenInput,TextInput

class XMPPSettingsForm(ModelForm):
    class Meta:
        model = StreamXMPPSettings
        fields = ["community","enabled","server","domain","streams","conference","pubsub","endpoint","self_reg","auto_group"]
        widgets = {
            "uuid":HiddenInput(),
            "community":HiddenInput(),
            "server":TextInput(),
            "streams": TextInput(),
            "conference": TextInput(),
            "pubsub": TextInput(),
            "endpoint":TextInput(),
            "domain": TextInput()
        }

from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField

from communities.stream.models import StreamXMPPSettings
from django import forms
from django.forms.widgets import SelectDateWidget,HiddenInput,TextInput

class XMPPSettingsForm(ModelForm):
    class Meta:
        model = StreamXMPPSettings
        fields = ["community","enabled","server","endpoint"]
        widgets = {
            "uuid":HiddenInput(),
            "community":HiddenInput(),
            "server":TextInput(),
            "endpoint":TextInput()
        }

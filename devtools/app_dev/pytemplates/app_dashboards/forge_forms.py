from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField

from ufls.event.models import Event,EventCommunityMapping
from django import forms
from django.forms.widgets import SelectDateWidget,HiddenInput
from django.forms import ModelForm,CharField,TextInput,Textarea,CheckboxInput,HiddenInput,Select
from .models import Preferences,Timezone,Theme
import pytz

class PreferencesForm(ModelForm):
    def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

    class Meta:
        model = Preferences
        fields = [ "shortdate", "longdate", "time", "timezone", "theme", "stream_top","messages_top","user"]

        help_texts = {
            'shortdate': ('Example value: "03/05/2022" Default: "%x" (Accepts Python strftime formatting)'),
            'longdate': ('Example value: "Mon Sep 30 07:06:05 2020" Default: "%c" (Accepts Python strftime formatting)'),
            'time': ('Example value: "07:06:05" Default: "%I:%M:%S" (Accepts Python strftime formatting)'),
            'timezone':('Select your Current Timezone; times are expressed relative to this value.'),
            'theme':('Select your System Theme/skin.'),
            'stream_top':('Scroll/add content to streams Top-down? (Twitter-like) - Check to Enable'),
            'messages_top':('Scroll/add content to Messages/conversations Top-down? (Twitter-like) - Check to Enable'),
        }
        error_messages = {
            'name': {
                'blank': ("Cannot be blank!"),
            },
        },
        widgets = {
            'shortdate': TextInput(attrs={}),
            'longdate': TextInput(attrs={}),
            'time': TextInput(attrs={}),
            'stream_top':CheckboxInput(attrs={'class':'switch'}),
            'messages_top':CheckboxInput(attrs={'class':'switch'}),
            'user': HiddenInput(attrs={}),
            'timezone':Select(attrs={}),
            'theme':Select(attrs={}),


        }



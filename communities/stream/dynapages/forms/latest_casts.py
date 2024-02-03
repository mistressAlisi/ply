from django import forms
from ply.toolkit import profiles
class WidgetForm(forms.Form):
    profile = False
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
            self.profile = profiles.get_active_profile(request)
        super().__init__(*args, **kwargs)
    count = forms.IntegerField(label='Number of Posts :',min_value=1,max_value=10,initial=5)


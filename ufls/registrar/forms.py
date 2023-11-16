from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField
from ufls.registrar.models import Registrant, RegistrantLevel
from django import forms
from django.forms.widgets import NumberInput,EmailInput,CheckboxInput,Select
from communities.profiles.models import Profile
class RegistrantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrantForm, self).__init__(*args, **kwargs)
        self.fields['level'].queryset = RegistrantLevel.objects.filter(active=True)
        self.fields['profile'] = ChoiceField(choices=[('','Login to associate a profile with this registration!')])

    def load_profiles(self,community,user):
        qs = Profile.objects.filter(active=True,community=community,creator=user)
        self.fields['profile'] = ModelChoiceField(queryset=qs)
    class Meta:
        model = Registrant
        fields = ["firstName", "lastName", "email","profile","phone","country","addr1","addr2","city","state","zip","dob","level", "badgeName", "fdDonation","chDonation"]
        widgets = {
                   'dob': NumberInput(attrs={'type': 'date'}),
                   'email':EmailInput()
                   }


class ConditionsForm(ModelForm):
    class Meta:
        model = Registrant
        fields = ["agreeCOC","agreeRFP","agreeCVD"]
        labels = {
                'agreeCOC': 'I agree to the Code of Conduct.',
                'agreeRFP': 'I agree to the Refund Policy.',
                'agreeCVD': 'I agree to the COVID Policy.'
        }




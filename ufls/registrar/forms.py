from django.db import models
from django.forms import ModelForm,ChoiceField,ModelChoiceField
from ufls.registrar.models import Registrant, RegistrantLevel
from django import forms
from django.forms.widgets import NumberInput,EmailInput,CheckboxInput,Select
from communities.profiles.models import Profile
from communities.community.models import ProfilePerCoummunityView
class RegistrantForm(ModelForm):
    def __init__(self,*args,user=None,community=None,  **kwargs):
        super(RegistrantForm, self).__init__(*args, **kwargs)
        self.fields['level'].queryset = RegistrantLevel.objects.filter(active=True)
        if user is not None:
            self.load_profiles(community,user)
        else:
            self.fields['profile'] = ChoiceField(choices=[('','Login to associate a profile with this registration!')])

    def load_profiles(self,community,user):
        cv = ProfilePerCoummunityView.objects.filter(system=False,frozen=False,community=community,creator=user).values_list('uuid')
        qs = Profile.objects.filter(uuid__in=cv)
        self.fields['profile'] = ModelChoiceField(queryset=qs,to_field_name="uuid")
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




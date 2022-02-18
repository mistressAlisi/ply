from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ "name", "age", "status", "species", "introduction", "pronouns","gender","archived","blocked","frozen","system","dynapage","profile_id"]
        

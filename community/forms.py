

from django.forms import ModelForm
from .models import Community

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = [ "name", "action_call_cover", "tagline", "introduction", "backgroundItem","archived","blocked","frozen","system","hash"]
        

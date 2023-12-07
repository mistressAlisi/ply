

from django.forms import ModelForm,HiddenInput
from .models import Community,CommunityStaff
from communities.profiles.models import Profile
class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = [ "name", "action_call_cover", "tagline", "introduction", "backgroundItem","archived","blocked","frozen","system","hash"]


class CommunityStaffForm(ModelForm):
    class Meta:
        model = CommunityStaff
        fields = ["community","profile","active"]

    def __init__(self,  *args, **kwargs):
        super(CommunityStaffForm, self).__init__(*args, **kwargs)
        self.fields['community'].widget = HiddenInput()

    def set_community(self,community):
        if isinstance(community,Community):
            self.fields['community'].initial = community.pk
        self.fields["profile"].queryset = Profile.objects.filter(system=False)




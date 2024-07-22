from django.forms import ModelForm, HiddenInput, TextInput
from .models import Community, CommunityStaff, CommunityAdmins, CommunitySidebarMenu
from communities.profiles.models import Profile


class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = [
            "name",
            "action_call_cover",
            "tagline",
            "introduction",
            "backgroundItem",
            "archived",
            "blocked",
            "frozen",
            "system",
            "hash",
            "theme"

        ]


class CommunityStaffForm(ModelForm):
    class Meta:
        model = CommunityStaff
        fields = ["community", "profile", "active"]

    def __init__(self, *args, **kwargs):
        super(CommunityStaffForm, self).__init__(*args, **kwargs)
        self.fields["community"].widget = HiddenInput()

    def set_community(self, community):
        if isinstance(community, Community):
            self.fields["community"].initial = community.pk
        self.fields["profile"].queryset = Profile.objects.filter(system=False)


class CommunityAdminForm(ModelForm):
    class Meta:
        model = CommunityAdmins
        fields = ["community", "profile", "active"]

    def __init__(self, *args, **kwargs):
        super(CommunityAdminForm, self).__init__(*args, **kwargs)
        self.fields["community"].widget = HiddenInput()

    def set_community(self, community):
        if isinstance(community, Community):
            self.fields["community"].initial = community.pk
        self.fields["profile"].queryset = Profile.objects.filter(system=False)


class CommunitySidebarMenuForm(ModelForm):
    class Meta:
        model = CommunitySidebarMenu
        fields = [
            "uuid",
            "community",
            "application_mode",
            "module",
            "sidebar_class",
            "ordering",
            "active",
            "not_edited",
        ]

    def __init__(self, *args, **kwargs):
        super(CommunitySidebarMenuForm, self).__init__(*args, **kwargs)
        self.fields["community"].widget = HiddenInput()
        self.fields["not_edited"].widget = HiddenInput()
        self.fields["uuid"].widget = HiddenInput()
        # self.fields["application_mode"].widget = TextInput()
        self.fields["sidebar_class"].widget = TextInput()

    def set_community(self, community):
        if isinstance(community, Community):
            self.fields["community"].initial = community.pk

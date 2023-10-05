import datetime

from django import forms

from .models import StaffApplication


class StaffApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffApplicationForm, self).__init__(*args, **kwargs)
        self.fields["openPosition"].widget = forms.HiddenInput()
        self.fields["closeApp"].widget = forms.HiddenInput()

        year = datetime.datetime.today().year

        self.fields["dateOfBirth"].widget = forms.SelectDateWidget(
            years=range(year, year - 100, -1)
        )

    class Meta:
        model = StaffApplication
        fields = "__all__"

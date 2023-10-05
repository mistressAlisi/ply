import datetime

from django import forms

from .models import StaffOnboardRecord


class StaffOnboardRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffOnboardRecordForm, self).__init__(*args, **kwargs)
        self.fields["openPosition"].widget = forms.HiddenInput()

        year = datetime.datetime.today().year

        self.fields["dateOfBirth"].widget = forms.SelectDateWidget(
            years=range(year, year - 100, -1)
        )

    class Meta:
        model = StaffOnboardRecord
        fields = "__all__"

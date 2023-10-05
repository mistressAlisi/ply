from django import forms

class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label='New Password', max_length=100)
    confirmPassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', max_length=100)
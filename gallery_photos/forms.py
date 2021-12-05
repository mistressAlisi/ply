from django import forms
from django.forms import ModelForm,DateInput,Textarea,TextInput,Form,ClearableFileInput,Select
from datetime import datetime
from ply.toolkit import ratings
from gallery.toolkit import settings

class upload_form(forms.Form):
    image = forms.ImageField(widget=ClearableFileInput(attrs={"id":"upload-files-widget","multiple":"true"}))

# REMEMBER to pass a RESOLUTIONS object which contains valid resolution choices for the item being reviewed!!!
class review_form(forms.Form):
    title = forms.CharField(widget=TextInput(attrs={"id":"review-title"}),label="Title:")
    descr = forms.CharField(widget=Textarea(attrs={"id":"review-descr",'rows':2}),label="Description:")
    resolution = forms.ChoiceField(widget=Select(attrs={"id":"review-resolution"}),label="Max Resolution:")
    raiting = forms.ChoiceField(choices=ratings.RATING_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-raiting"}),label="Raiting:")
    nsfw = forms.ChoiceField(choices=ratings.NSFW_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-nsfw"}),label="NSFW:")
    display_style = forms.ChoiceField(choices=settings.DISPLAY_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_style"}),label="Display Style:")
    display_sizing = forms.ChoiceField(choices=settings.SIZING_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_sizing"}),label="Sizing Hint:")
    display_details = forms.ChoiceField(choices=settings.DETAILS_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_details"}),label="Details:")
    publish_notify = forms.ChoiceField(choices=settings.PUBLISH_NOTIFY_CHOICES,widget=Select(attrs={"id":"review-publish_notify"}),label="Notify:")
    publish_keywords = forms.ChoiceField(widget=Select(attrs={"id":"review-publish_keywords"}),label="Keywords:")
    publish_category = forms.ChoiceField(widget=Select(attrs={"id":"review-publish_category"}),label="Category:")
    publish_collections = forms.ChoiceField(widget=Select(attrs={"id":"review-publish_collections"}),label="Initial Collection(s):")
    


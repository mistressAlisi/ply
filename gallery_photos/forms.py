from django import forms
from django.forms import ModelForm,DateInput,Textarea,TextInput,Form,ClearableFileInput,Select,CheckboxInput,HiddenInput
from datetime import datetime
from ply.toolkit import ratings
from gallery.toolkit import settings
from keywords.models import Keyword
from gallery.models import GalleryItemKeyword



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
    

class details_form(forms.Form):
    def __init__(self,*args,**kwargs):
        if 'item' in kwargs:
            item = kwargs.pop('item')
            super(details_form,self).__init__(*args,**kwargs)
            self.fields['title'].initial = item.title
            self.fields['descr'].initial = item.descr
            self.fields['uuid'].initial = item.uuid
            self.fields['plugin'].initial = item.plugin
            kwo = GalleryItemKeyword.objects.filter(item=item)
            val = ""
            for k in kwo:
                val += f"#{k.keyword.hash},"

            self.fields["gr_keywords"].initial = val[:-1]
        else:
            super(details_form,self).__init__(*args,**kwargs)
    uuid = forms.CharField(widget=HiddenInput(attrs={"id":"uuid"}))
    plugin = forms.CharField(widget=HiddenInput(attrs={"id":"plugin"}))
    title = forms.CharField(widget=TextInput(attrs={"id":"review-title"}),label="Title:")
    descr = forms.CharField(widget=Textarea(attrs={"id":"review-descr",'rows':2}),label="Description:")
    gr_category = forms.CharField(widget=TextInput(attrs={"id":"gr_category"}),label="Category:")
    gr_keywords = forms.ChoiceField(widget=TextInput(attrs={"id":"gr_keywords"}),label="Keywords:")



class settings_form(forms.Form):
    display_style = forms.ChoiceField(choices=settings.DISPLAY_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_style"}),label="Display Style:")
    display_sizing = forms.ChoiceField(choices=settings.SIZING_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_sizing"}),label="Sizing Hint:")
    display_details = forms.ChoiceField(choices=settings.DETAILS_SUBMISSION_CHOICES,widget=Select(attrs={"id":"review-display_details"}),label="Details:")
    resolution = forms.ChoiceField(widget=Select(attrs={"id":"review-resolution"}),label="Gallery Resolution:")
    enable_comments = forms.BooleanField(widget=CheckboxInput(attrs={"id":"comments"}),label="Enable Comments?",help_text="Can Users Leave Comments?",required=False)
    enable_sharing = forms.BooleanField(widget=CheckboxInput(attrs={"id":"comments"}),label="Enable Sharing?",help_text="Can Users Share this?",required=False)
    enable_download = forms.BooleanField(widget=CheckboxInput(attrs={"id":"download"}),label="Enable Download?",help_text="Enable Downloading of rescaled file?",required=False)
    download_resolution = forms.ChoiceField(widget=Select(attrs={"id":"download-resolution"}),label="Download Resolution:")

from django import forms
import json
from django.forms import (
    Textarea,
    TextInput,
    ClearableFileInput,
    Select,
    CheckboxInput,
    HiddenInput,
)
from ply.toolkit import ratings
from media.gallery.core.toolkit import settings
from media.gallery.core.models import GalleryItemKeyword
from content_manager.categories.models import Category


class upload_form(forms.Form):
    image = forms.ImageField(
        widget=ClearableFileInput(attrs={"id": "upload-files-widget"})
    )


# REMEMBER to pass a RESOLUTIONS object which contains valid resolution choices for the item being reviewed!!!
class review_form(forms.Form):
    title = forms.CharField(
        widget=TextInput(attrs={"id": "review-title"}), label="Title:"
    )
    descr = forms.CharField(
        widget=Textarea(attrs={"id": "review-descr", "rows": 2}), label="Description:"
    )
    resolution = forms.ChoiceField(
        widget=Select(attrs={"id": "review-resolution"}), label="Resolution:"
    )
    raiting = forms.ChoiceField(
        choices=ratings.RATING_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "review-raiting"}),
        label="Rating:",
    )
    nsfw = forms.ChoiceField(
        choices=ratings.NSFW_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "review-nsfw"}),
        label="NSFW:",
    )
    display_style = forms.ChoiceField(
        choices=settings.DISPLAY_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "review-display_style"}),
        label="Display Style:",
    )
    display_sizing = forms.ChoiceField(
        choices=settings.SIZING_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "review-display_sizing"}),
        label="Sizing:",
    )
    display_details = forms.ChoiceField(
        choices=settings.DETAILS_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "review-display_details"}),
        label="Details:",
    )
    publish_notify = forms.ChoiceField(
        choices=settings.PUBLISH_NOTIFY_CHOICES,
        widget=Select(attrs={"id": "review-publish_notify"}),
        label="Notify:",
    )
    publish_keywords = forms.ChoiceField(
        widget=Select(attrs={"id": "review-publish_keywords"}), label="Keywords:"
    )
    publish_category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("discipline"),
        widget=Select(attrs={"id": "review-publish_category"}),
        label="Category:",
    )
    publish_collections = forms.ChoiceField(
        widget=Select(attrs={"id": "review-publish_collections"}),
        label="Initial Collection(s):",
    )

    def setup_form(self, item):
        if "title" in item.userdata:
            self.fields["title"].initial = item.userdata["title"]
        else:
            self.fields["title"].initial = item.name
        # print(item.userdata)
        if "descr" in item.userdata:
            self.fields["descr"].initial = item.userdata["descr"]
        else:
            self.fields["descr"].initial = f"A beautiful new image by {item.profile.name}."
        h = item.meta["metadata"]["height"]
        w = item.meta["metadata"]["width"]
        scale = 1.0
        CHOICES = []
        while scale > 0.1:
            CHOICES.append(
                (
                    round(scale, 1),
                    f"{round(w*scale)}x{round(h*scale)}",
                )
            )
            scale -= 0.1
        self.fields["resolution"].choices = CHOICES
        select_fields = ["resolution","raiting","display_style","display_sizing","publish_notify","display_details","nsfw"]
        for f in select_fields:
            if f in item.userdata:
                self.fields[f].initial = item.userdata[f]


class details_form(forms.Form):
    def __init__(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs.pop("item")
            super(details_form, self).__init__(*args, **kwargs)
            self.fields["title"].initial = item.title
            self.fields["descr"].initial = item.descr
            self.fields["uuid"].initial = item.uuid
            self.fields["plugin"].initial = item.plugin
            self.fields["gr_category"].initial = item.category
            kwo = GalleryItemKeyword.objects.filter(item=item)
            val = ""
            for k in kwo:
                val += f"{k.keyword.hash},"

            self.fields["gr_keywords"].initial = val[:-1]
        else:
            super(details_form, self).__init__(*args, **kwargs)

    uuid = forms.CharField(widget=HiddenInput(attrs={"id": "uuid"}))
    plugin = forms.CharField(widget=HiddenInput(attrs={"id": "plugin"}))
    title = forms.CharField(
        widget=TextInput(attrs={"id": "review-title"}), label="Title:"
    )
    descr = forms.CharField(
        widget=Textarea(attrs={"id": "review-descr", "rows": 2}), label="Description:"
    )
    gr_category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("discipline"),
        widget=Select(attrs={"id": "gr_category"}),
        label="Category:",
    )
    gr_keywords = forms.CharField(
        widget=TextInput(attrs={"id": "gr_keywords"}), label="Keywords:"
    )


class settings_form(forms.Form):
    def __init__(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs.pop("item")
            if type(item.plugin_data) is str:
                id = json.loads(item.plugin_data)
            else:
                id = item.plugin_data
            h = id["metadata"]["height"]
            w = id["metadata"]["width"]
            scale = 1.0
            CHOICES = []
            while scale > 0.1:
                CHOICES.append(
                    (
                        round(scale, 1),
                        f"[W: {round(w*scale)}px * H: {round(h*scale)}px]",
                    )
                )
                scale -= 0.1
            super(settings_form, self).__init__(*args, **kwargs)
            self.fields["sizing"].choices = CHOICES
            self.fields["down_size"].choices = CHOICES
            self.fields["en_comments"].initial = item.en_comments
            self.fields["en_sharing"].initial = item.en_sharing
            self.fields["en_download"].initial = item.en_download
            self.fields["detail_style"].initial = item.detail_style
            self.fields["sizing_hint"].initial = item.sizing_hint
            self.fields["display_details"].initial = item.display_details
            self.fields["plugin"].initial = item.plugin
            self.fields["uuid"].initial = item.uuid
            if "sizing" in id:
                self.fields["sizing"].initial = id["sizing"]
            else:
                self.fields["sizing"].initial = 1.0
            if "down_size" in id:
                self.fields["down_size"].initial = id["down_size"]
            else:
                self.fields["down_size"].initial = 1.0

        else:
            super(settings_form, self).__init__(*args, **kwargs)

    uuid = forms.CharField(widget=HiddenInput(attrs={"id": "uuid"}))
    plugin = forms.CharField(widget=HiddenInput(attrs={"id": "plugin"}))
    detail_style = forms.ChoiceField(
        choices=settings.DISPLAY_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "detail_style"}),
        label="Display Style:",
    )
    sizing_hint = forms.ChoiceField(
        choices=settings.SIZING_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "sizing_hint"}),
        label="Sizing:",
    )
    display_details = forms.ChoiceField(
        choices=settings.DETAILS_SUBMISSION_CHOICES,
        widget=Select(attrs={"id": "display_details"}),
        label="Display Details:",
    )
    sizing = forms.ChoiceField(
        widget=Select(attrs={"id": "sizing"}), label="Gallery Resolution:"
    )
    en_comments = forms.BooleanField(
        widget=CheckboxInput(attrs={"id": "en_comments"}),
        label="Enable Comments?",
        help_text="Can Users Leave Comments?",
        required=False,
    )
    en_sharing = forms.BooleanField(
        widget=CheckboxInput(attrs={"id": "en_sharing"}),
        label="Enable Sharing?",
        help_text="Can Users Share this?",
        required=False,
    )
    en_download = forms.BooleanField(
        widget=CheckboxInput(attrs={"id": "en_download"}),
        label="Enable Download?",
        help_text="Enable Downloading of rescaled file?",
        required=False,
    )
    down_size = forms.ChoiceField(
        widget=Select(attrs={"id": "down_size"}), label="Download Resolution:"
    )

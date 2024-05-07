from django.forms import ModelForm, HiddenInput

from media.gallery.images.models import GalleryImagesSettings

class Forge_Form(ModelForm):
    class Meta:
        model = GalleryImagesSettings
        fields = ["max_filesize","enable_exif","enable_icc","min_dpi","rescaler_enabled","enabled_filetypes","rescaler_factor","rescaler_target_format","rescaler_fallback_jpeg","rescaler_target_quality","downloads_enabled","community"]
    def __init__(self, *args, **kwargs):
        super(Forge_Form, self).__init__(*args, **kwargs)
        self.fields["community"].widget = HiddenInput()
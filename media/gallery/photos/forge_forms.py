from django.forms import ModelForm, HiddenInput

from media.gallery.photos.models import GalleryPhotoSettings

class Forge_Form(ModelForm):
    class Meta:
        model = GalleryPhotoSettings
        fields = ["gallery_max_filesize","enable_exif","community"]
    def __init__(self, *args, **kwargs):
        super(Forge_Form, self).__init__(*args, **kwargs)
        self.fields["community"].widget = HiddenInput()
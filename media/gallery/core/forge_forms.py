from django.forms import ModelForm
from media.gallery.core.models import GalleryCoreSettings


class CoreSettingsForm(ModelForm):
    class Meta:
        model = GalleryCoreSettings
        fields = ["enable_gallery","enable_stream_integration","enable_stream_integration","enable_fed_publishing","enable_rss_publishing","enable_group_galleries","gallery_max_filesize","enabled_plugins"]
import ply
from media.gallery.core.models import GalleryCoreSettings
from media.gallery.images.models import GalleryImagesSettings


class gallery_upload_plugin:
    def __init__(self, community):
        self.content_type_info = (
            {
                "label": "Images",
                "id": "media.gallery.images",
                "icon": "fas fa-photo-video",
                "desc": "The Images plugin provides galleries for visual artwork from all types of mediums.",
                "upload_form": "gallery_photos_upload_form.html",
                "review_form": "gallery_photos_review_form.html",
            },
        )
        global_settings = GalleryCoreSettings.objects.get(community=community)

        plugin_settings = GalleryImagesSettings.objects.get(community=community)
        content_accept_filetypes = plugin_settings.enabled_filetypes.all()
        self.content_accept_filetypes_str = ""
        self.content_accept_filetypes = []
        for caf in content_accept_filetypes:
            for cf in caf.ext.split(","):
                    self.content_accept_filetypes.append(cf)
            self.content_accept_filetypes_str += caf.ext + ","
        self.content_accept_filetypes_str = self.content_accept_filetypes_str[:-1]

        if global_settings.gallery_max_filesize <= plugin_settings.max_filesize:
            self.content_max_file_size_kb = global_settings.gallery_max_filesize
        else:
            self.content_max_file_size_kb = plugin_settings.gallery_max_filesize

#!/usr/bin/env python3
# The Navigation component dotes the Console with the ability to auto-generate sidebar and top menus based on the installed and registered Ceres Modules.
import importlib

from django.conf.urls import include
import ply
from media.gallery.core.models import GalleryCoreSettings


class upload_plugins_builder:
    modules = {}

    def __init__(self, community, plugin=False):
        if len(self.modules) is 0:
            gallery_settings = GalleryCoreSettings.objects.get(community=community)
            plugins = gallery_settings.enabled_plugins.all()
            if not plugin:
                self.register(plugins, community)
            else:
                self.register([x for x in plugins if x.app == plugin], community)

    # Register a module to the sidebar, pass it's Module.Navigation class to this constructor:
    def register(self, data, community):
        if data is False:
            raise ValueError(
                "UploadButtonBuilder must recieve a PLY_GALLERY_PLUGINS object!"
            )
        for mname in data:
            import_module = importlib.import_module(f"{mname.app}.gallery_upload")
            gup_data = import_module.gallery_upload_plugin(community)
            self.modules[mname.app] = gup_data

"""
toolkit/gallery.py
====================================
Toolkit utilities for interacting with Galleries:
"""
import importlib
import uuid

from django.utils.text import slugify

from communities.community.models import Community, Friend, Follower
from media.gallery.core.models import (
    GalleryCoreSettings,
    GalleryCollection,
    GalleryCollectionPermission,
)


def get_active_accepted_filetypes(community):
    gallery_settings = GalleryCoreSettings.objects.get(community=community)
    plugins = gallery_settings.enabled_plugins.all()
    return_data = []
    for plugin in plugins:
        plugin_settings_obj = importlib.import_module(
            f"{plugin.app}.models"
        ).__galleryGetSettingsObject()
        plugin_settings = plugin_settings_obj.objects.get(community=community)
        filetypes = plugin_settings.enabled_filetypes.all()
        filetypedata = []
        for file in filetypes:
            filetypedata += file.ext.split(",")
        if gallery_settings.gallery_max_filesize <= plugin_settings.max_filesize:
            max_size = gallery_settings.gallery_max_filesize
        else:
            max_size = plugin_settings.max_filesize
        metadata_mod = importlib.import_module(f"{plugin.app}.metadata")
        return_data.append(
            {
                "plugin": plugin.app,
                "filetypes": filetypedata,
                "max_size": max_size,
                "metadata_mod": metadata_mod,
            }
        )
    return return_data


def create_collection(profile, community, label, slug=False):
    """Create Collection:"""
    if slug is False:
        slug = slugify(label)
    col = GalleryCollection.objects.get_or_create(
        label=label, collection_id=slug, owner=profile
    )[0]
    perm = GalleryCollectionPermission.objects.get_or_create(
        collection=col, profile=profile, owner=True, community=community
    )[0]
    col.save()
    perm.save()
    return col, perm

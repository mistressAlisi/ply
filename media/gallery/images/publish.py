import io
import json
from communities.profiles.models import Profile

from PIL import Image
from pillow_heif import register_heif_opener
import pillow_avif

from media.gallery.images.utilities import get_image_encoder_settings

register_heif_opener()

import hashlib, pathlib
from ply import settings
from media.gallery.images.models import GalleryImagesSettings
from ply.toolkit import file_uploader, logger as plylog
from media.gallery.images.toolkit import settings as gsettings
from media.gallery.images import utilities
from media.gallery.core.models import GalleryItemFile
from core.metrics.models import UserDataEntry

log = plylog.getLogger("media.gallery.images.publish", name="publish")


def publish_submission(
    data_str, profile, temp_file, original_path, item, user, community, temp_file_id
):
    # Step one: Calculate the maximum size based on user input:
    mdata = json.loads(data_str["meta"])["metadata"]
    sizing = float(data_str["display_sizing"])
    # ftemp = os.path.splitext(temp_file)
    fvar = pathlib.Path(temp_file)
    sha1 = hashlib.sha1()
    output_formats = get_image_encoder_settings(community)
    # Step two: Open the file...
    with Image.open(temp_file) as im:
        # Generate scaled images first, based on our settings:
        if im.width > im.height:
            largest_side = im.width * sizing
        else:
            largest_side = im.height * sizing
        for ts in gsettings.IMAGE_THUMBNAIL_SIZES:
            if ts <= largest_side:
                tsp = f"{item.uuid}/{profile.profile_id}-{fvar.stem}-th_{ts}"
                thumb = im.copy()
                thumb.thumbnail([ts, ts])

                for format in output_formats:
                    isp = f"{tsp}.{format}"
                    thumb_file = io.BytesIO()
                    thumb.save(thumb_file, format)
                    sha1.update(thumb_file.read())
                    name, tss = file_uploader.save_gallery_file(thumb_file, profile, isp)
                    GalleryItemFile.objects.create(
                        name=tsp,
                        item=item,
                        type=format,
                        hash=sha1.hexdigest(),
                        file_size=tss,
                        meta=mdata,
                        thumbnail=True,
                    )
                    UserDataEntry.objects.create(
                        user=user,
                        community=community,
                        category="gallery_item",
                        bytes=tss,
                        reference=tsp,
                    )
                    # ftp = mdata["format"]
                    log.info(
                        f"File Scaled and encoded in Gallery Storage: {isp} (Format: {format}): Profile: {profile.uuid} [{round(tss/1024,2)} kB] saved."
                    )
                    # thumb.save(tsp)
        # Step 3: Now scale and save the full core image:
        ispr = f"{item.uuid}/{profile.profile_id}-{fvar.stem}"
        for format in output_formats:
            isp = f"{ispr}.{format}"
            thumb_file = io.BytesIO()
            im.thumbnail([sizing * im.width, sizing * im.height])
            im.save(thumb_file, format)
            sha1.update(thumb_file.read())
            name, iss = file_uploader.save_original_file(thumb_file, profile, isp)
            GalleryItemFile.objects.create(
                name=isp,
                item=item,
                type=format,
                hash=sha1.hexdigest(),
                file_size=iss,
                meta=mdata,
            )
            UserDataEntry.objects.create(
                user=user,
                community=community,
                category="gallery_item",
                bytes=iss,
                reference=isp,
            )
            log.info(
                f"File Stored in Gallery Storage: {isp}: Profile: {profile.uuid} [{round(iss/1024,2)} kB] saved."
            )
        # Step 4: Now clean up stale files that are no longer needed:
        # upload_cleaner.delay(profile.uuid,temp_file_id)


def update_submission(item,community):
    if type(item.plugin_data) == "str":
        id = json.loads(item.plugin_data)
    else:
        id = item.plugin_data
    sizing = float(id["sizing"])
    original = GalleryItemFile.objects.get(original=True, item=item)
    output_formats = get_image_encoder_settings(community)
    ori_path = file_uploader.get_temp_path(original.name, item.profile)
    ifile = file_uploader.get_original_file(ori_path)
    with Image.open(ifile) as im:
        sha1 = hashlib.sha1()
        if sizing < 1.0:
            im.thumbnail([sizing * im.width, sizing * im.height])
            for format in output_formats:
                filedata = io.BytesIO()
                im.save(filedata, format)
                sha1.update(filedata.read())
                name, iss = utilities.save_gallery_photo(
                    filedata, item.profile, original.name
                )
                fileitm = GalleryItemFile.objects.get(
                    original=False, item=item, thumbnail=False
                )
                fileitm.hash = sha1.hexdigest()
                fileitm.file_size = iss
                fileitm.save()
                log.info(
                    f"File Updated in Gallery Storage: {original.name}: Profile: {item.profile.uuid} New size: [{round(iss/1024,2)} kB] Sizing factor: {sizing}."
                )

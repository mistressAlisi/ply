import json
from PIL import Image
import ply
import os
import hashlib,pathlib




from ply.toolkit import vhosts,file_uploader,logger as plylog
from gallery_photos.toolkit import settings as gsettings
from gallery_photos import utilities
from gallery.models import GalleryItemFile
from metrics.models import UserDataEntry
from gallery.tasks import upload_cleaner

log = plylog.getLogger('gallery_photos.publish',name='gallery_photos.publish')
def publish_submission(data_str,profile,temp_file,original_path,item,user,community,temp_file_id):
    # Step one: Caclculate the maximum size based on user input:
    mdata = json.loads(data_str["meta"])["metadata"]
    sizing = float(data_str["sizing"])
    #ftemp = os.path.splitext(temp_file)
    fvar = pathlib.Path(temp_file)
    
    # Step two: Open the file...
    with Image.open(temp_file) as im:
        # Generate Thumbnails first, based on our settings:
        if (im.width > im.height):
            largest_side = im.width * sizing
        else:
            largest_side = im.height * sizing
        for ts in gsettings.IMAGE_THUMBNAIL_SIZES:
            if (ts <= largest_side):
                sha1 = hashlib.sha1()
                tsp =  f"{profile.slug}-{fvar.stem}-th_{ts}{fvar.suffix}"
                thumb = im.copy()
                thumb.thumbnail([ts,ts])
                sha1.update(im.tobytes())
                thumb.format = im.format
                tss = utilities.save_gallery_photo(thumb,profile,tsp)
                GalleryItemFile.objects.create(name=tsp,item=item,type=mdata["format"],hash=sha1.hexdigest(),file_size=tss,meta=mdata,thumbnail=True)
                UserDataEntry.objects.create(user=user,community=community,category="gallery_item",bytes=tss,reference=tsp)
                ftp =  mdata["format"]
                log.info(f"File Thumbnailed in Gallery Storage: {tsp}: Profile: {profile.uuid} [{round(tss/1024,2)} kB] saved.")
                #thumb.save(tsp)
        # Step 3: Now scale and save the full gallery image:
        sha1 = hashlib.sha1()
        isp = f"{profile.slug}-{fvar.stem}{fvar.suffix}"
        im.thumbnail([sizing*im.width,sizing*im.height])
        sha1.update(im.tobytes())
        iss = utilities.save_gallery_photo(im,profile,isp)
        GalleryItemFile.objects.create(name=isp,item=item,type=mdata["format"],hash=sha1.hexdigest(),file_size=iss,meta=mdata)
        UserDataEntry.objects.create(user=user,community=community,category="gallery_item",bytes=iss,reference=isp)
        log.info(f"File Stored in Gallery Storage: {isp}: Profile: {profile.uuid} [{round(iss/1024,2)} kB] saved.")
        # Step 4: Now clean up stale files that are no longer needed:
        upload_cleaner(profile.uuid,temp_file_id)
        


from PIL import Image
import ply
import os
import hashlib
from ply.toolkit import vhosts,file_uploader,logger as plylog
from gallery_photos.toolkit import settings as gsettings
from gallery_photos import utilities
from gallery.models import GalleryItemFile
import json
from metrics.models import UserDataEntry
log = plylog.getLogger('gallery_photos.publish',name='gallery_photos.publish')
def publish_submission(data_str,profile,original_path,item,user,community):
    # Step one: Caclculate the maximum size based on user input:
    mdata = json.loads(data_str["meta"])["metadata"]
    sizing = float(data_str["sizing"])
    ftemp = os.path.splitext(original_path)
    fvar = (os.path.basename(ftemp[0]), ftemp[1])
    
    # Step two: Open the file...
    with Image.open(original_path) as im:
        # Generate Thumbnails first, based on our settings:
        if (im.width > im.height):
            largest_side = im.width * sizing
        else:
            largest_side = im.height * sizing
        for ts in gsettings.IMAGE_THUMBNAIL_SIZES:
            if (ts <= largest_side):
                sha1 = hashlib.sha1()
                tsp =  f"{profile.slug}-{fvar[0]}-th_{ts}{fvar[1]}"
                thumb = im.copy()
                thumb.thumbnail([ts,ts])
                sha1.update(im.tobytes())
                tss = utilities.save_gallery_photo(thumb,profile,tsp)
                GalleryItemFile.objects.create(name=tsp,item=item,type=mdata["format"],hash=sha1.hexdigest(),file_size=tss,meta=mdata,thumbnail=True)
                UserDataEntry.objects.create(user=user,community=community,category="gallery_item",bytes=tss,reference=tsp)
                ftp =  mdata["format"]
                log.info(f"File Thumbnailed in Gallery Storage: {tsp}: Profile: {profile.uuid} [{round(tss/1024,2)} kB] saved.")
                #thumb.save(tsp)
        # Step 3: Now scale and save the full gallery image:
        sha1 = hashlib.sha1()
        isp = f"{profile.slug}-{fvar[0]}{fvar[1]}"
        im.thumbnail([sizing*im.width,sizing*im.height])
        sha1.update(im.tobytes())
        iss = utilities.save_gallery_photo(im,profile,isp)
        GalleryItemFile.objects.create(name=isp,item=item,type=mdata["format"],hash=sha1.hexdigest(),file_size=iss,meta=mdata)
        UserDataEntry.objects.create(user=user,community=community,category="gallery_item",bytes=iss,reference=isp)
        log.info(f"File Stored in Gallery Storage: {isp}: Profile: {profile.uuid} [{round(iss/1024,2)} kB] saved.")
            
        


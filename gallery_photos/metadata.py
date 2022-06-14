from PIL import Image
import pathlib,json,os

# PLY
import ply
from ply.toolkit import vhosts,file_uploader,logger as plylog
from gallery_photos import utilities
from ply import settings
from gallery.models import GalleryTempFileThumb

log = plylog.getLogger('gallery_photos.metadata',name='gallery_photos.metadata')

def thumbnail(profile,file,file_obj):
    #print(file.name)
    #fullpath = ply.settings.PLY_TEMP_FILE_BASE_PATH+file_uploader.get_temp_path(file.name,profile)
    fullpath = pathlib.Path(file.name)
    #print(fullpath)
    name = f"{fullpath.stem}_thumb{fullpath.suffix}"

        
    #print(name)
    #print("*****")
    #print("*****")
    #print("*****")
    tpath = file_uploader.get_temp_path(name,profile)
    fulltpath = ply.settings.PLY_TEMP_FILE_BASE_PATH+tpath

    try:
        with Image.open(file.name) as im:
            try:
                im.thumbnail([settings.GALLERY_PHOTOS_THUMBNAIL_SIZE,settings.GALLERY_PHOTOS_THUMBNAIL_SIZE])
                im.save(fulltpath)
                im.close()
                #file.thumbnail = tpath
                #file.save()
                tempFileObj = GalleryTempFileThumb(file=file_obj,path=tpath,file_size=im.tell())
                tempFileObj.save()
            except Exception as e:
                 log.exception(e)
                 log.error(f"With Image Open: Unable to generate Thumbnail for {file}: Exception: {e}")
                 return None
    except Exception as e:
        log.exception(e)
        log.error(f"Unable to generate Thumbnail for {file}: Exception: {e}")
        return None
    return tpath
                
def initial_import_gen(relpath,ret_image=False):
    path = ply.settings.PLY_TEMP_FILE_BASE_PATH+relpath
    try:
        with Image.open(path) as im:
            try:
                exif_dict = utilities.generate_exif_dict(im)
                exif_data = {}
                for k in exif_dict.keys():
                #print(exif_dict[k])
                    try:
                        dump = json.dumps(exif_dict[k]["processed"])
                    except Exception as e:
                        dump = None
                    finally:
                        exif_data[k] = dump
            except Exception:
                exif_data = {}
            return_data = {"metadata":{"name":im.filename,
             "width":im.width,
             "height":im.height,
             "format":im.format,
             "exif":exif_data
             }}
            if "dpi" in im.info:
                return_data["dpi"] = int(im.info["dpi"][0])
            
            
            if ret_image is False:
                im.close()
                return(return_data)
            else:
                return([return_data,im])
            
    except Exception as e:
        log.error(f"Unable to generate Metadata for {path}: Exception: {e}")
        return None
    
        

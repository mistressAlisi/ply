
from django.shortcuts import render
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ply.toolkit import vhosts,file_uploader,logger as plylog,streams as streams_toolkit
from gallery.uploader import upload_plugins_builder
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q
from gallery.models import GalleryTempFile,GalleryCatGroupObject,GalleryArtworkCat,GalleryCatGroups,GalleryCatGroupObject,GalleryCollectionPermission
from profiles.models import Profile
from metrics.models import UserDataEntry
import json,uuid,importlib,ply
from celery import shared_task,Celery
from ply.toolkit import file_uploader
from django.db import IntegrityError, transaction
from gallery.models import GalleryItem,GalleryItemFile,GalleryArtworkCat,GalleryItemCategory,GalleryItemKeyword,GalleryCollectionItems,GalleryCollection,GalleryCollectionPermission,GalleryTempFileThumb
from metrics.models import UserDataEntry
from django.utils.text import slugify
import os
import hashlib,shutil,logging
from keywords.models import Keyword
from django.core.exceptions import ValidationError
from community.models import Community
from categories.models import Category
import ply,boto3,io
log = plylog.getLogger('gallery.tasks',name='gallery.tasks')
app = Celery('ply')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings')

@app.task
@transaction.atomic
#(request.POST,profile.uuid,temp_file.id,request.user.id,comm.uuid)
def publish_to_gallery(data,profile,temp_file,user,community):
    try:
        profile = Profile.objects.get(uuid=profile)
        community = Community.objects.get(uuid=community)
        temp_file = GalleryTempFile.objects.get(id=temp_file)
        user = User.objects.get(id=user)
        # Import the right plugin and let it do it's thing:
        publish_mod = importlib.import_module(f"{temp_file.plugin}.publish")
        # Step one: Move the original file to the original storage:
        temp_path = ply.settings.PLY_TEMP_FILE_BASE_PATH+file_uploader.get_temp_path(temp_file.name,profile)
        original_path = ply.settings.PLY_GALLERY_ORIGINAL_FILE_BASE_PATH+file_uploader.get_temp_path(temp_file.name,profile)
        try:
            temp_file_handle = open(temp_path,'rb')
            fsize = file_uploader.save_original_file(temp_file_handle,profile)
            item_hash = slugify(data["title"])
            catitem = Category.objects.get(pk=data["cat"])
            item = GalleryItem.objects.create(uuid=uuid.uuid4(),item_hash=item_hash,profile=profile,plugin=data["plugin"],nsfw=data["nsfw"],rating=data["rating"],title=data["title"],descr=data["descr"],sizing=data["sizing"],plugin_data=data["meta"],category=catitem)
            # Step three: Register the original file (hash it first):
            sha1 = hashlib.sha1()
            while True:
                fdata = temp_file_handle.read(ply.settings.PLY_GALLERY_HASH_BUF_SIZE)
                if not fdata:
                    break
                sha1.update(fdata)
                fsize = temp_file_handle.tell()
            temp_file_handle.close()
            
            GalleryItemFile.objects.create(item=item,type=temp_file.meta["metadata"]["format"],hash=sha1.hexdigest(),file_size=fsize,meta=temp_file.meta,original=True,name=f"{profile.profile_id}-{temp_file.name}")
            UserDataEntry.objects.create(user=user,community=community,category="gallery_item",bytes=fsize,reference=temp_file.name)
            # Step three: Use the imported plugin module to process the file for the galleries and create files:
            publish_mod.publish_submission(data,profile,temp_path,original_path,item,user,community,temp_file.id)
            # Step Four: Add to collections:
            for c in data["cat"].split(","):
                cat = GalleryArtworkCat.objects.get_or_create(label=c)[0]
                gic = GalleryItemCategory.objects.get_or_create(item=item,category=cat)[0]
                gic.save()
                cat.save()
            # Step Five: Add to Keywords:
            for k in data["kw"].split(","):
                if (len(k)>1):
                    if (k[0] == "#"):
                        hs = f"#{slugify(k[1:])}"
                        ekw = Keyword.objects.get_or_create(hash=k)
                        if (ekw[1] is True):
                            ekw[0].keyword = k[1:]
                        kw = ekw[0]
                    else:
                        hs = "#"+slugify(k)
                        kw = Keyword.objects.get_or_create(keyword=k,hash=hs)[0]
                    gkw = GalleryItemKeyword.objects.get_or_create(item=item,keyword=kw)[0]
                    gkw.save()
                    kw.save()
            # Step six: Add to Collections:
            for c in data["col"].split(","):
                try:
                    col = GalleryCollection.objects.get_or_create(uuid=c)[0]
                except ValidationError:
                    col = GalleryCollection.objects.get_or_create(label=c,collection_id=slugify(c))[0]
                # Don't forget the permissions object!
                colc = GalleryCollectionPermission.objects.get_or_create(collection=col,profile=profile,owner=True,community=community)[0]
            
                # Now add the items...
                gic = GalleryCollectionItems.objects.get_or_create(item=item,collection=col)[0]

            
                # And save all:
                col.save()
                gic.save()
                colc.save()
                cat.save()
            # Step Seven: Notifications
            # TODO: implement :
            # Step Eight: Streams!
            streams_toolkit.post_to_profile_stream(profile,community,"application/ply.stream.gallery",'<i class="fa-solid fa-retweet"></i> Recasted from Gallery!',{"col":str(col.uuid),"item":str(item.uuid)})
        except Exception as e:
            log.exception(e)
            return False
        finally:
            # WARNING: this is for debug, for production os.rename is preferred.
            # WARNING: This path appears to be not necessary anymore, save_original_file above suffices.

            #shutil.copy(temp_path,original_path)
            
            #Step Eight: Cleanup
            #os.remove(temp_path)
            #temp_file.delete()
            return True
    except Exception as e:
            print(e)
            log.error(f"File Uploader: Unable to generate Publish file {temp_file} to gallery: {e}")
            logging.exception(e)
            #transaction.rollback()
            
@app.task
@transaction.atomic
def upload_ingest(_profile,plugin,file_name,filepath,_file_obj,content_type="",size=1):
    try:
        profile = Profile.objects.get(uuid=_profile)
        file_obj = GalleryTempFile.objects.get(id=_file_obj)
        #plugin = request.POST['plugin']
        #file = request.FILES[file_name]
        # Depending on our plugin, let's load a Metadata Processor:
        # for the classes that require preprocessing like thumbnailing;
        # it should happen inside initial_import_gen below:
        metadata_mod = importlib.import_module(f"{plugin}.metadata")
        # And get our metadata and image:
        fpoint = open(ply.settings.PLY_TEMP_FILE_BASE_PATH+filepath)
        thumb = metadata_mod.thumbnail(profile,fpoint,file_obj)
        file_obj.thumbnail = thumb
        file_obj.path = file_uploader.get_temp_path(f"{profile.profile_id}-{file_obj.name}",profile)
        file_obj.save()
        tempFileObj = GalleryTempFileThumb(file=file_obj,path=file_obj.path,file_size=size)
        tempFileObj.save()
        log.info(f"File Thumbnailed in Temporary Storage: {file_name}. Content type: {content_type}. {profile} [{round(size/1024,2)} kB] saved.")
    except Exception as e:
            log.exception(e)
            log.error(f"File Uploader: Unable to generate Thumbnail for file {file_name}: {e}")
            #transaction.rollback()


@app.task
@transaction.atomic
def upload_cleaner(_profile,_file_obj):
    try:
        profile = Profile.objects.get(uuid=_profile)
        file_obj = GalleryTempFile.objects.get(id=_file_obj)
        # Delete the original temp file:
        os.unlink(ply.settings.PLY_TEMP_FILE_BASE_PATH+file_obj.path)
        # and the Temp files:
        tempFileObj = GalleryTempFileThumb.objects.filter(file=file_obj)
        for tF in tempFileObj:
            os.unlink(ply.settings.PLY_TEMP_FILE_BASE_PATH+tF.path)
            tF.delete()
        # finally, DB cleanup:
        file_obj.delete()
        log.info(f"File in Temporary Storage: {file_obj.path} hasa been removed.")
    except Exception as e:
            log.exception(e)
            log.error(f"File Uploader: Unable to remove temp file: {file_obj.path}: {e}")
            #transaction.rollback()



@app.task
@transaction.atomic
def remove_item(_profile,_item):
    try:
        profile = Profile.objects.get(uuid=_profile)
        item_obj = GalleryItem.objects.get(uuid=_item)
        if (item_obj.profile != profile):
            return False
        files = GalleryItemFile.objects.filter(item=item_obj)
        log.info(f"Item in Main Storage: {item_obj.uuid} being deleted...")
        if (ply.settings.PLY_AVATAR_STORAGE_USE_S3 == 'TRUE'):
            s3client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        for file in files:
            # Delete the file:
            keystr= f'{ply.settings.PLY_GALLERY_FILE_BASE_PATH}/{file.name}'
            if (ply.settings.PLY_AVATAR_STORAGE_USE_S3 == 'TRUE'):
                s3client.delete_object(Bucket=ply.settings.AWS_STORAGE_BUCKET_NAME, Key=keystr)
            else:
                os.unlink(keystr)
            file.delete()
        item_obj.delete()

    except Exception as e:
            log.exception(e)
            log.error(f"Item Removal: Unable to remove item file: {_item}: {e}")
            #transaction.rollback()


@app.task
@transaction.atomic
def update_submission_files(_item_obj):
    item = GalleryItem.objects.get(uuid=_item_obj)
    plugin_mod = importlib.import_module(f"{item.plugin}.publish")
    plugin_mod.update_submission(item)
    item.save()



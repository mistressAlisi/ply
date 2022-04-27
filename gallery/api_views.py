from django.shortcuts import render
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,file_uploader,logger as plylog
from gallery.uploader import upload_plugins_builder
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q
from gallery.models import GalleryTempFile,GalleryCatGroupObject,GalleryArtworkCat,GalleryCatGroups,GalleryCatGroupObject,GalleryCollectionPermission,GalleryItem,GalleryCollection
from gallery import serialisers
from gallery.tasks import publish_to_gallery,upload_ingest
from profiles.models import Profile
from community.models import Community
from metrics.models import GalleryItemHit
from metrics import toolkit as metrics_toolkit
import json
import ply
import importlib

log = plylog.getLogger('gallery.api_views',name='gallery.api_views')
#queue = GalleryPublisher(ply.settings.PLY_MSG_BROKER_URL,log)
#queue.start()


@login_required
def get_form(request,plugin):
    plugins = upload_plugins_builder()
    template = plugins.modules[plugin].content_type_info[0]['upload_form']
    forms = include(plugin+'.forms')[0]
    context = {'plugin':plugins.modules[plugin],'upload_form':forms.upload_form,'filetypes':plugins.modules[plugin].content_accept_filetypes,'filesize':plugins.modules[plugin].content_max_file_size_kb}
    return render(request,template,context)
    
@login_required
@transaction.atomic
def post_upload_thumbs(request):

    return JsonResponse("ok",safe=False)

@login_required
@transaction.atomic
def post_upload(request):
    profile = Profile.objects.get(uuid=request.session['profile'])
    plugin = request.POST['plugin']
    for file_name in request.FILES:
        try:
            file = request.FILES[file_name]
            relpath = file_uploader.save_temp_file(file,profile)
            # Depending on our plugin, let's load a Metadata Processor:
            # for the classes that require preprocessing like thumbnailing;
            # it should happen inside initial_import_gen below:
            metadata_mod = importlib.import_module(f"{plugin}.metadata")
            # And get our metadata and image:
            imported = metadata_mod.initial_import_gen(relpath)
            obj = GalleryTempFile.objects.create(name=file.name,profile=profile,type=file.content_type,plugin=plugin,file_size=file.size,meta=imported)
            obj.save()
            relpath = file_uploader.save_temp_file(file,profile)
            # Background processing after quick import:
            upload_ingest.delay(profile.uuid,plugin,file_name,relpath,obj.id,file.content_type,file.size)
            log.warn(f"File uploaded into Temporary Storage: {file.name}. Content type: {file.content_type}. Profile: {request.session['profile']} [{round(file.size/1024,2)} kB] saved.")
        except Exception as e:
            print(e)
            log.error(f"File Uploader: Unable to save file {file_name}: {e}")
            #transaction.rollback()
    return JsonResponse("ok",safe=False)   

@login_required
def get_categories(request):
    categories = GalleryCatGroupObject.objects.filter(active=True,hidden=False,archived=False)
    cat_json = {}
    for cat in categories:
        if cat.group.group_id not in cat_json:
            cat_json[cat.group.group_id] = {}
            cat_json[cat.group.group_id]["__label"] = cat.group.label
        if cat.category.cat_id not in cat_json[cat.group.group_id]:
            cat_json[cat.group.group_id][cat.category.cat_id] = {}
        cat_json[cat.group.group_id][cat.category.cat_id] = cat.category.label
        
    return JsonResponse(cat_json,safe=False)

@login_required
def get_review_panel(request,file_id):
    try:
        temp_file = GalleryTempFile.objects.get(id=file_id)
    except:
            log.error(f"File Uploader: Unable to find temp file {file_id} in database.")
            return JsonResponse("error: File not found in TempDB.",safe=False)
    if (str(temp_file.profile.uuid) != request.session['profile']):
            log.error(f"**SECURITY ERROR: Profile {request.session['profile']} tried to access File #{file_id} from TempDB; which does not belong to that profile: Request rejected!")
            return JsonResponse("File Uploader: Unable to proceed - Security Context is inconsistent with expected environment",safe=False)          
    plugins = upload_plugins_builder()
    template = plugins.modules[temp_file.plugin].content_type_info[0]['review_form']
    forms = include(temp_file.plugin+'.forms')[0]
    review_form = forms.review_form()
    context = {'plugin':plugins.modules[temp_file.plugin],'review_form':review_form,'filetypes':json.dumps(plugins.modules[temp_file.plugin].content_accept_filetypes),'temp_file':temp_file,'low_dpi_thrs':ply.settings.PLY_GALLERY_MIN_DPI}
    return render(request,template,context)

@login_required
def get_collections_writeable(request):
    col_json = {"cols":{}}
    profile = Profile.objects.filter(pk=request.session['profile'])
    collections = GalleryCollectionPermission.objects.filter(profile=request.session['profile'],community=request.session['community']).filter( Q(owner=True) | Q(edit=True) | Q(create=True))
    for col in collections:
        col_json["cols"][str(col.collection.uuid)] = col.collection.label
    return JsonResponse(col_json,safe=False)


@login_required
def publish_after_review(request,file_id):
    try:
        temp_file = GalleryTempFile.objects.get(id=file_id)
    except:
            log.error(f"File Uploader: Unable to find temp file {file_id} in database.")
            return JsonResponse("error: File not found in TempDB.",safe=False)
    if (str(temp_file.profile.uuid) != request.session['profile']):
            log.error(f"**SECURITY ERROR: Profile {request.session['profile']} tried to access File #{file_id} from TempDB; which does not belong to that profile: Request rejected!")
            return JsonResponse("File Uploader: Unable to proceed - Security Context is inconsistent with expected environment",safe=False)          
    profile = Profile.objects.get(uuid=request.session['profile'])
    comm = Community.objects.get(uuid=request.session["community"])
    publish_to_gallery.delay(request.POST,profile.uuid,temp_file.id,request.user.id,comm.uuid)
    return JsonResponse("ok",safe=False)

# Get ALL The items for the active request session profile:
# Where the session is also the owner of the item:
@login_required
def gallery_collections_raw(request):
    colls = serialisers.serialise_profile_collection_items(request,True)
    profile = Profile.objects.get(uuid=request.session["profile"])
    return JsonResponse(colls,safe=False)   

# Get ALL The items for the specified Collection (where the specified profile is the owner)
#@login_required
def gallery_collection_items_raw(request,collection):
    colls = serialisers.serialise_per_collection_items(request,collection)
    #profile = Profile.objects.get(uuid=request.session["profile"])
    return JsonResponse(colls,safe=False)   

@transaction.atomic
def gallery_viewer_counter_item(request):
    comm = Community.objects.get(uuid=request.session["community"])
    if ('itm' in request.GET):
        iid = request.GET['itm']
        item = GalleryItem.objects.get(pk=iid)
        itemHit = GalleryItemHit.objects.create(item=item,community=comm,type="VIEW")
        metrics.toolkit.request_data_capture(request,itemHit)
        item.views = item.views + 1;
        item.save();
    if ('col' in request.GET):
        cid = request.GET['col']
        col = GalleryCollection.objects.get(pk=cid)
        col.views = item.views + 1;
        col.save();
    return JsonResponse("ok",safe=False)

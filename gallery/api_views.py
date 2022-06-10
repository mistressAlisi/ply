from django.shortcuts import render
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,file_uploader,logger as plylog,reqtools
from gallery.uploader import upload_plugins_builder
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q
from gallery.models import GalleryTempFile,GalleryCatGroupObject,GalleryArtworkCat,GalleryCatGroups,GalleryCatGroupObject,GalleryCollectionPermission,GalleryItem,GalleryCollection,GalleryTempFileThumb,GalleryCollectionItems,GalleryItemFile
from gallery import serialisers,forms
from gallery.tasks import publish_to_gallery,upload_ingest,remove_item
from profiles.models import Profile
from community.models import Community
from metrics.models import GalleryItemHit
from metrics.toolkit import request_data_capture
import metrics
from ply.toolkit.reqtools import vhost_community_or_404
from ply.toolkit import streams as stream_toolkit,file_uploader,profiles as toolkit_profiles
import json
import ply
import importlib
import os
from django.utils.text import slugify


from django.contrib.auth.hashers import check_password
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
        request_data_capture(request,itemHit)
        item.views = item.views + 1;
        item.save();
    if ('col' in request.GET):
        cid = request.GET['col']
        col = GalleryCollection.objects.get(pk=cid)
        col.views = item.views + 1;
        col.save();
    return JsonResponse("ok",safe=False)


@transaction.atomic
def gallery_share_counter_item(request):
    comm = Community.objects.get(uuid=request.session["community"])
    if ('itm' in request.GET):
        iid = request.GET['itm']
        item = GalleryItem.objects.get(pk=iid)
        itemHit = GalleryItemHit.objects.create(item=item,community=comm,type="SHARE")
        request_data_capture(request,itemHit)
        item.shares = item.shares + 1;
        item.save();
    if ('col' in request.GET):
        cid = request.GET['col']
        col = GalleryCollection.objects.get(pk=cid)
        col.shares = item.shares + 1;
        col.save();
    return JsonResponse("ok",safe=False)


@login_required
@transaction.atomic
def gallery_recast_item(request,col,item):
    """
    @brief Recast a given Item in a given collection into the logged in profile's stream
    :param request: p_request:Django Request
    :type request: t_request:str
    :param col: p_col:Collection
    :type col: t_col:UUID
    :param item: p_item:ITEM
    :type item: t_item:UUID
    :returns: r:JsonResponse: OK or error and error data.
    """
    community = vhost_community_or_404(request)
    item = GalleryItem.objects.get(pk=item)
    itemHit = GalleryItemHit.objects.create(item=item,community=community,type="RECAST")
    request_data_capture(request,itemHit)
    item.shares = item.shares + 1;
    item.save();
    col = GalleryCollection.objects.get(pk=col)
    col.shares = item.shares + 1;
    col.save();
    message = stream_toolkit.post_to_active_profile(request,"application/ply.stream.gallery",'<i class="fa-solid fa-retweet"></i> Recasted from Gallery!',{"col":str(col.uuid),"item":str(item.uuid)})
    return JsonResponse("ok",safe=False)




@login_required
@transaction.atomic
def gallery_toggle_invisible(request,item):
    item = GalleryItem.objects.get(pk=item)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    if (item.archived == True):
        item.archived = False;
        item.save();
        return JsonResponse("vis",safe=False)
    elif (item.archived == False):
        item.archived = True;
        item.save();
        return JsonResponse("invis",safe=False)


@login_required
@transaction.atomic
def gallery_remove_temp(request,item):
    item = GalleryTempFile.objects.get(pk=item)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    thumbs = GalleryTempFileThumb.objects.filter(file=item)
    for thumb in thumbs:
        path = file_uploader.get_temp_path(thumb.path,item.profile)
        destpath = ply.settings.PLY_TEMP_FILE_BASE_PATH+path
        try:
            os.unlink(destpath)
        except FileNotFoundError:
            log.warn(f"Deleting Temp item {thumb.path} - the file was not found in the Filesystem. Deleting SQL node anyway.")
        thumb.delete()
    path = file_uploader.get_temp_path(item.path,item.profile)
    destpath = ply.settings.PLY_TEMP_FILE_BASE_PATH+path
    try:
        os.unlink(destpath+"/"+item.path)
    except FileNotFoundError:
        log.warn(f"Deleting Temp item {item.path} - the file was not found in the Filesystem. Deleting SQL node anyway.")
    item.delete();


    return JsonResponse("ok",safe=False)




@login_required
def gallery_copymove_form(request,item,col):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    item = GalleryItem.objects.get(pk=item)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    profile = toolkit_profiles.get_active_profile(request)
    moveForm = forms.copy_move_form(profile=profile,community=community,item=item.uuid,icol=col)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'move_form':moveForm}
    return render(request,"gallery/card_api/copy_move_form.html",context)


@login_required
@transaction.atomic
def gallery_copymove_exec(request):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    col = request.POST["collection"]

    ncol = request.POST["new_collection"]
    if (col == "-1" and ncol == "") :
        return JsonResponse({"res":"err","err":"Must specify new collection name!"},safe=False)
    i = request.POST["item"]
    op = request.POST["operation"]
    icol = request.POST["icol"]
    if (icol == ncol):
        return JsonResponse({"res":"err","err":"Must specify a different collection!"},safe=False)
    profile = toolkit_profiles.get_active_profile(request)
    item = GalleryItem.objects.get(pk=i)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    if (col == "-1"):
        """ Create Collection: """
        col = GalleryCollection.objects.get_or_create(label=ncol,collection_id=slugify(ncol))[0]
        colc = GalleryCollectionPermission.objects.get_or_create(collection=col,profile=profile,owner=True,community=community)[0]
        col.save()
        colc.save()
    else:
        col = GalleryCollection.objects.get(uuid=col)
    if (op == "c"):
        """ COPY to a new collection: """
        gic = GalleryCollectionItems.objects.get_or_create(item=item,collection=col)[0]
        gic.save()
    elif (op == "m"):
        """ MOVE to a new collection: """
        gic = GalleryCollectionItems.objects.get_or_create(item=item,collection=col)[0]
        gic.save()

        icol = GalleryCollection.objects.get(uuid=icol)
        oldcols = GalleryCollectionItems.objects.get(item=item,collection=icol)
        oldcols.delete()

    if "cast_to_stream" in request.POST:
        if (request.POST["cast_to_stream"] == "on"):
            message = stream_toolkit.post_to_active_profile(request,"application/ply.stream.gallery",'<i class="fa-solid fa-retweet"></i> Casted from Gallery!',{"col":str(col.uuid),"item":str(item.uuid)})
    return JsonResponse("ok",safe=False)


@login_required
def gallery_remitem_form(request,item,col):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    item = GalleryItem.objects.get(pk=item)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    profile = toolkit_profiles.get_active_profile(request)
    colitems = GalleryCollectionItems.objects.filter(item=item)
    ccol = GalleryCollection.objects.get(uuid=col)
    removeForm = forms.remove_form(profile=profile,community=community,item=item.uuid,icol=ccol)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'remove_form':removeForm,'item':item,'colitems':colitems}
    return render(request,"gallery/card_api/remove_form.html",context)

@login_required
@transaction.atomic
def gallery_remove_exec(request):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    icol = request.POST["icol"]
    item = request.POST["item"]
    op = request.POST["operation"]
    item_name = request.POST["item_name"]
    confirm = request.POST["confirm"]
    item = GalleryItem.objects.get(pk=item)
    profile = toolkit_profiles.get_active_profile(request)
    if (item_name != str(item.uuid)[:4]):
        return JsonResponse({"res":"err","err":"Please enter the first 4 chars of the item ID."},safe=False)
    if check_password(request.POST["pw"],request.user.password) is False:
        return JsonResponse({"res":"err","err":"Bad Password."},safe=False)
    if (str(item.profile.uuid) != request.session['profile']):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    if (confirm != "on"):
        return JsonResponse({"res":"err","err":"Confirm it."},safe=False)
    if (op == "r"):
        """ if op is R, it means ALL collection instances are to be nuked - and then the item item itself: """
        colitems = GalleryCollectionItems.objects.filter(item=item)
        colitems.delete()
        remove_item(str(profile.uuid),str(item.uuid))


    elif (op == "i"):
        """ Only the initial collection item will be deleted; if there are no more collection items, THEN we will nuke the item itself:"""
        icol = GalleryCollection.objects.get(uuid=icol)
        colitems = GalleryCollectionItems.objects.filter(item=item,collection=icol)
        colitems.delete()
        colitems = GalleryCollectionItems.objects.filter(item=item)
        if (len(colitems) == 0):
            remove_item(str(profile.uuid),str(item.uuid))


    return JsonResponse("ok",safe=False)



@login_required
def gallery_settings_form(request,item,col):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    item = GalleryItem.objects.get(pk=item)
    profile = toolkit_profiles.get_active_profile(request)
    if (str(item.profile.uuid) != str(profile.uuid)):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)
    colitems = GalleryCollectionItems.objects.filter(item=item)
    ccol = GalleryCollection.objects.get(uuid=col)
    removeForm = forms.remove_form(profile=profile,community=community,item=item.uuid,icol=ccol)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'remove_form':removeForm,'item':item,'colitems':colitems}
    return render(request,"gallery/card_api/settings_form.html",context)




@login_required
def gallery_item_metadata(request,item,col):
    vhost = request.META["HTTP_HOST"];
    community = vhosts.get_vhost_community(hostname=vhost)
    item = GalleryItem.objects.get(pk=item)
    profile = toolkit_profiles.get_active_profile(request)
    if (str(item.profile.uuid) != str(profile.uuid)):
        return JsonResponse({"res":"err","err":"Access denied."},safe=False)

    colitems = GalleryCollectionItems.objects.filter(item=item)
    colfiles = GalleryItemFile.objects.filter(item=item)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'item':item,'colitems':colitems,'colfiles':colfiles}
    return render(request,"gallery/card_api/metadata.html",context)

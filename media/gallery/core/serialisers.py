from media.gallery.core.models import GalleryItemsByCollectionPermission
import ply


def _item_serialiser(_items):
    items = []
    total = len(_items)
    counter = 0
    curr_items = []
    curr_files = []
    for i in _items:
        uuidstr = str(i.profile_uuid);
        #print(f"{i.item_id}\n{uuidstr}\n->>{uuidstr[0:1]}/{uuidstr[1:2]}/{uuidstr[2:3]}/{uuidstr}\n******************")
        curr_files.append({
            "id":i.gif_id,
            'item':i.gci_uuid,
            "name":i.gif_name,
            "hash":i.gif_hash,
            "created":i.gif_created,
            "updated":i.gif_updated,
            "meta":i.gif_meta,
            "thumbnail":i.gif_thumbnail,
            "size":i.gif_size,
            "original":i.gif_original,
            'plugin':i.gci_plugin,
            "path": f"{ply.settings.PLY_GALLERY_FILE_URL_BASE_URL}/{uuidstr[0:1]}/{uuidstr[1:2]}/{uuidstr[2:3]}/{uuidstr}/{i.gif_name}"
        })
        if (counter+1 < total):
            if (i.item_id != _items[counter+1].item_id):
                #print("Item change here.")
                # PUT thumbnail first.... 
                curr_files.reverse()
                curr_items.append({'plugin':i.gci_plugin,'plugin_data':i.gci_plugin_data,'title':i.gci_title,'descr':i.gci_descr,'likes':i.gci_likes,'views':i.gci_views,'shares':i.gci_shares,'comments':i.gci_comments,'downloads':i.gci_downloads,'details':i.gci_details,'sizing':i.gci_sizing,'style':i.gci_style,'rating':i.gci_rating,'nsfw':i.gci_nsfw,'files':curr_files,'profile':{"uuid":str(i.profile_uuid),"name":i.profile_name,"pronouns":i.profile_pronouns,"avatar":i.profile_avatar,"slug":i.profile_slug},'id':i.gci_uuid,'created':i.gci_created,'archived':i.gci_archived,'counter':counter})
                curr_files = []
            if (i.collection_id != _items[counter+1].collection_id):
                #print("Collection change here.")
                items.append({
                    "label":i.gc_label,
                    "created":i.gc_created,
                    "updated":i.gc_updated,
                    "items":i.gc_items,
                    "views":i.gc_views,
                    "likes":i.gc_likes,
                    "shares":i.gc_shares,
                    "comments":i.gc_comments,
                    "uuid":i.gc_uuid,
                    "collection_id":i.gc_id,
                    "items":curr_items
                    })
                curr_items = []
            #print(_items[counter+1].item_id)    
        else:
            #print("final Item and Collection flush")
            # PUT thumbnail first.... 
            curr_files.reverse()
            curr_items.append({'plugin':i.gci_plugin,'plugin_data':i.gci_plugin_data,'title':i.gci_title,'descr':i.gci_descr,'likes':i.gci_likes,'views':i.gci_views,'shares':i.gci_shares,'comments':i.gci_comments,'downloads':i.gci_downloads,'details':i.gci_details,'sizing':i.gci_sizing,'style':i.gci_style,'rating':i.gci_rating,'nsfw':i.gci_nsfw,'files':curr_files,'profile':{"uuid":str(i.profile_uuid),"name":i.profile_name,"pronouns":i.profile_pronouns,"avatar":i.profile_avatar,"slug":i.profile_slug},'id':i.gci_uuid,'created':i.gci_created,'archived':i.gci_archived,'counter':counter})
            curr_files = []
            items.append({
                    "label":i.gc_label,
                    "created":i.gc_created,
                    "updated":i.gc_updated,
                    "items":i.gc_items,
                    "views":i.gc_views,
                    "likes":i.gc_likes,
                    "shares":i.gc_shares,
                    "comments":i.gc_comments,
                    "uuid":i.gc_uuid,
                    "collection_id":i.gc_id,
                    "items":curr_items,
                    
                    })
            curr_items = []
        #print("*****")
        counter += 1
    #print(f"Total: {total}, Counter: {counter}")
    return items


# Get ALL The items for the active request session profile:
# Where the session is also the owner of the item:
def serialise_profile_collection_items(request):
    _items = GalleryItemsByCollectionPermission.objects.filter(gcp_profile=request.session['profile'],gcp_owner=True).order_by("gc_uuid").distinct()
    return (_item_serialiser(_items))
   
# Get ALL The items for the specified Collection (where the session profile is the owner)
def serialise_own_collection_items(request,collection):
    _items = GalleryItemsByCollectionPermission.objects.filter(gcp_profile=request.session['profile'],gcp_owner=True,gc_uuid=collection).order_by("gc_uuid").distinct()
    return (_item_serialiser(_items))
   
# Get ALL The items for the community (filters apply here):
def serialise_community_items(request):
    _items = GalleryItemsByCollectionPermission.objects.filter(gcp_community=request.session['community']).order_by("gc_uuid").distinct()
    return (_item_serialiser(_items))


# Get ALL The items for the specified profile inside the specified community (filters apply here - if you specify collection it will also filter by collection):
def serialise_community_per_profile_items(request,profile,collection=False):
    if (collection is False):
        _items = GalleryItemsByCollectionPermission.objects.filter(gcp_community=request.session['community'],gcp_profile=profile.uuid).order_by("gc_uuid").distinct()
    else:
        _items = GalleryItemsByCollectionPermission.objects.filter(gcp_community=request.session['community'],gcp_profile=profile.uuid,gc_uuid=collection.uuid).order_by("gc_uuid").distinct()
    return (_item_serialiser(_items))


# Get ALL The items for the specified profile inside the specified collection (filters apply here):
def serialise_per_collection_items(request,collection_id):
    _items = GalleryItemsByCollectionPermission.objects.filter(gcp_community=request.session['community'],gc_uuid=collection_id).order_by("gc_uuid").distinct()
    return (_item_serialiser(_items))


from django.db import models
from django.contrib import admin
from profiles.models import Profile
from community.models import Community
from group.models import Group
from keywords.models import Keyword

import uuid,json

# Create your models here.
class GalleryType(models.Model):
    type_id = models.TextField(max_length=200,verbose_name='Type ID')
    label = models.TextField(max_length=200,verbose_name='Type Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Type Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Type Updated')
    items = models.IntegerField(verbose_name='Item Count',null=True,blank=True,default=0)
    def __str__(self):
        return f"Gallery Type: {self.label}"
    
@admin.register(GalleryType)
class GalleryTypeAdmin(admin.ModelAdmin):
    pass

class GalleryArtworkCat(models.Model):
    cat_id = models.TextField(max_length=200,verbose_name='Cat ID')
    label = models.TextField(max_length=200,verbose_name='Cat Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Cat Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Cat Updated')
    items = models.IntegerField(verbose_name='Item Count',null=True,blank=True,default=0)
    def __str__(self):
        return f"Gallery Artwork Category: {self.label}"
    
@admin.register(GalleryArtworkCat)
class GalleryArtworkCatAdmin(admin.ModelAdmin):
    pass


class GalleryCatGroups(models.Model):
    group_id = models.TextField(max_length=200,verbose_name='Group ID')
    label = models.TextField(max_length=200,verbose_name='Group Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Group Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Group Updated')
    items = models.IntegerField(verbose_name='Item Count',null=True,blank=True,default=0)
    categories = models.IntegerField(verbose_name='Category Count',null=True,blank=True,default=0)
    def __str__(self):
        return f"Gallery Category Groups: {self.label}"
    
@admin.register(GalleryCatGroups)
class GalleryCatGroupsAdmin(admin.ModelAdmin):
    pass

class GalleryCatGroupObject(models.Model):
    group = models.ForeignKey(GalleryCatGroups,verbose_name='Gallery Category Parent Group',on_delete=models.CASCADE)
    category = models.ForeignKey(GalleryArtworkCat,verbose_name='Gallery Category',on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name="Item Active Flag",default=True)
    archived = models.BooleanField(verbose_name="Item Archived Flag",default=False)
    hidden = models.BooleanField(verbose_name="Item Hidden Flag",default=False)
    frozen = models.BooleanField(verbose_name="Item Frozen Flag",default=False)   
    def __str__(self):
        return f"[{self.group.label} ({self.group.group_id})]->{self.category.label} ({self.category.cat_id})"    
@admin.register(GalleryCatGroupObject)
class GalleryCatGroupObjectAdmin(admin.ModelAdmin):
    pass



class GalleryItemTypes(models.Model):
    type_id = models.TextField(max_length=200,verbose_name='Type ID')
    label = models.TextField(max_length=200,verbose_name='Type Label')
    mimetypes = models.TextField(verbose_name='Type Mimetypes')
    service = models.TextField(max_length=200,verbose_name='Type Service Provider')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Type Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Type Updated')
    items = models.IntegerField(verbose_name='Item Count',null=True,blank=True,default=0)

@admin.register(GalleryItemTypes)
class GalleryItemTypesAdmin(admin.ModelAdmin):
    pass   


class GalleryItem(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    item_hash = models.TextField(max_length=200,verbose_name='Item Hash')
    title = models.TextField(max_length=200,verbose_name='Item Title')
    profile = models.ForeignKey(Profile,verbose_name='Item Owner',on_delete=models.RESTRICT)
    sizing = models.IntegerField(verbose_name='Sizing Hint',default=0)
    nsfw = models.CharField(verbose_name="Item NSFW Flag",default=False,max_length=10)
    details = models.CharField(verbose_name="Item Details Flags",default=False,max_length=10)
    style = models.CharField(verbose_name="Item Style Flag",default=False,max_length=10)
    rating = models.CharField(verbose_name="Item Rating",default=False,max_length=10)
    descr = models.TextField(max_length=200,verbose_name='Item Description')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Item Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='tem Updated')
    files = models.IntegerField(verbose_name='File Count',default=0)
    plugin = models.TextField(verbose_name="Item Plugin",default='',null=True)
    thumbnail = models.TextField(verbose_name="Item Thumbnail",default='',null=True)
    plugin_data = models.JSONField(verbose_name="Item plugin-specific data",blank=True,null=True)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    downloads = models.IntegerField(verbose_name='Download Count',default=0)
    likes = models.IntegerField(verbose_name='Likes Count',default=0)
    shares = models.IntegerField(verbose_name='Shares Count',default=0)
    comments = models.IntegerField(verbose_name='Comment Count',default=0)
    processed = models.BooleanField(verbose_name="Item has been processed",default=False)
    configured = models.BooleanField(verbose_name="Item has been configured (pre-processing)",default=False)
    active = models.BooleanField(verbose_name="Item Active Flag",default=True)
    archived = models.BooleanField(verbose_name="Item Archived Flag",default=False)
    hidden = models.BooleanField(verbose_name="Item Hidden Flag",default=False)
    frozen = models.BooleanField(verbose_name="Item Frozen Flag",default=False)
    def __str__(self):
        return f"Gallery Item: {self.uuid}, \"{self.title}\", plugin: {self.plugin}"
    
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    pass

class GalleryItemFile(models.Model):
    name = models.TextField(verbose_name='File Name')
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    hash = models.TextField(verbose_name='File Hash')
    type = models.TextField(verbose_name='File Type')
    data = models.TextField(verbose_name='File Data',blank=True,null=True)
    bindata = models.BinaryField(verbose_name='File Bindata',blank=True,null=True)
    jsondata = models.JSONField(verbose_name='File JSONData',blank=True,null=True)
    meta = models.JSONField(verbose_name='File Metadata')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    thumbnail = models.BooleanField(verbose_name="File is a thumbnail",default=False) 
    original = models.BooleanField(verbose_name="File is an Original",default=False) 
    file_size = models.FloatField(verbose_name='File Size',default=0)
    
    
    def __str__(self):
        return f"Gallery Item File: {self.name}"
    
@admin.register(GalleryItemFile)
class GalleryItemFileAdmin(admin.ModelAdmin):
    pass

class GalleryCollection(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    collection_id = models.TextField(max_length=200,verbose_name='Collection ID')
    label = models.TextField(max_length=200,verbose_name='Collection Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Collection Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Collection Updated')
    items = models.IntegerField(verbose_name='Item Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    likes = models.IntegerField(verbose_name='Likes Count',default=0)
    shares = models.IntegerField(verbose_name='Shares Count',default=0)
    comments = models.IntegerField(verbose_name='Comment Count',default=0)
    def __str__(self):
        return f"Gallery Collection: {self.label}"
    
@admin.register(GalleryCollection)
class GalleryCollectionAdmin(admin.ModelAdmin):
    pass

class GalleryCollectionItems(models.Model):
    collection = models.ForeignKey(GalleryCollection,verbose_name='Collection',on_delete=models.CASCADE)
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Gallery Item: {self.item.title} in Collection: {self.collection.label}"
@admin.register(GalleryCollectionItems)
class GalleryCollectionItemsAdmin(admin.ModelAdmin):
    pass
    
    
class GalleryItemCategory(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.RESTRICT)
    category = models.ForeignKey(GalleryArtworkCat,verbose_name='category',on_delete=models.RESTRICT)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Gallery Item: {self.item.title} in Category: {self.category.label}"
    
@admin.register(GalleryItemCategory)
class GalleryItemCategoryAdmin(admin.ModelAdmin):
    pass

class GalleryItemKeyword(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.RESTRICT)
    keyword = models.ForeignKey(Keyword,verbose_name='keyword',on_delete=models.RESTRICT)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)

@admin.register(GalleryItemKeyword)
class GalleryItemKeywordAdmin(admin.ModelAdmin):
    pass

class GalleryItemComments(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.RESTRICT)
    comment = models.TextField(verbose_name='Comment')
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    profile = models.ForeignKey(Profile,verbose_name='Item',on_delete=models.RESTRICT)
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    flagged = models.BooleanField(verbose_name="FLAGGED",default=False)
    def __str__(self):
        return f"Comment for Item: {item.label} by profile: {profile.name} on : {created}"
        
@admin.register(GalleryItemComments)
class GalleryItemCommentsAdmin(admin.ModelAdmin):
    pass
     
     
class GalleryCollectionPermission(models.Model):
    collection = models.ForeignKey(GalleryCollection,verbose_name="Gallery Collection",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True,blank=True)
    profile = models.ForeignKey(Profile,verbose_name='Profile',on_delete=models.RESTRICT,null=True)
    group = models.ForeignKey(Group,verbose_name='Group',on_delete=models.RESTRICT,null=True,blank=True)
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    owner = models.BooleanField(verbose_name="Owner FLAG",default=False)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    public = models.BooleanField(verbose_name="Publically Viewable",default=True)
    searchable = models.BooleanField(verbose_name="Show in Searches",default=True)
    shareable = models.BooleanField(verbose_name="Enable Sharing",default=True)
    create = models.BooleanField(verbose_name="Enable New Content Creation",default=False)
    comment = models.BooleanField(verbose_name="Enable Comments on Content",default=False)
    edit = models.BooleanField(verbose_name="Enable Content Editing",default=False)
    delete = models.BooleanField(verbose_name="Enable Content Deletion",default=False)
    nsfw = models.BooleanField(verbose_name="Enable NSFW Content Flag",default=False)
    explicit = models.BooleanField(verbose_name="Enable Explicit Content Flag",default=False)
    def __str__(self):
        if (self.community is not None):
            return f"Permissions for Collection: {self.collection.label}, profile: {self.profile.name}, group: {self.group}, in community: {self.community.name}"
        else:
            return f"Permissions for Collection: {self.collection.label}, profile: {self.profile.name}, group: {self.group}"
    
@admin.register(GalleryCollectionPermission)
class GalleryCollectionPermissionAdmin(admin.ModelAdmin):
    pass
     
     
     

class GalleryTempFile(models.Model):
    name = models.TextField(verbose_name='File Name')
    profile = models.ForeignKey(Profile,verbose_name='Profile',on_delete=models.RESTRICT,null=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    file_size = models.FloatField(verbose_name='File Size',default=0)
    type = models.TextField(verbose_name='File Type')
    thumbnail = models.TextField(verbose_name='File Thumbnail')
    plugin = models.TextField(verbose_name='File Plugin')
    path = models.TextField(verbose_name='File Path',blank=True,null=True)
    data = models.TextField(verbose_name='File Text Data',blank=True,null=True)
    bindata = models.BinaryField(verbose_name='File Bindata',blank=True,null=True)
    jsondata = models.JSONField(verbose_name='File JSONData',blank=True,null=True)
    meta = models.JSONField(verbose_name='File Metadata')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    published = models.BooleanField(verbose_name="Published FLAG",default=False)
    publish_job = models.UUIDField(verbose_name="Publish Job UUID",default=None,null=True)
    def __str__(self):
        return f"Gallery Item Temporary File: {self.name}"
    def get_meta_json(self):
        return str(json.dumps(self.meta))  
@admin.register(GalleryTempFile)
class GalleryTempFileAdmin(admin.ModelAdmin):
    pass
     
     
class GalleryTempFileCollections(models.Model):
    collection = models.ForeignKey(GalleryCollection,verbose_name='Collection',on_delete=models.CASCADE)
    file = models.ForeignKey(GalleryTempFile,verbose_name='Item',on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)


class GalleryTempFileKeywords(models.Model):
    file = models.ForeignKey(GalleryTempFile,verbose_name='Temp File',on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,verbose_name='keyword',on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    
    
class GalleryItemsByCollectionPermission(models.Model):
    gcp_id = models.IntegerField(verbose_name="Collection Permission ID")
    gcp_updated = models.DateTimeField(verbose_name="Collection Permission Updated")
    gcp_owner = models.BooleanField(verbose_name="Collection Permission Is Owner?")
    gcp_archived = models.BooleanField(verbose_name="Collection Permission Is Archived?")
    gcp_public = models.BooleanField(verbose_name="Collection Permission: Public?")
    gcp_searchable = models.BooleanField(verbose_name="Collection Permission: Is Searchable?")
    gcp_create = models.BooleanField(verbose_name="Collection Permission: Can create?")
    gcp_edit = models.BooleanField(verbose_name="Collection Permission: Can Edit?")
    gcp_delete = models.BooleanField(verbose_name="Collection Permission: Can Delete?")
    gcp_nsfw = models.BooleanField(verbose_name="Collection Permission: NSFW?")
    gcp_explicit = models.BooleanField(verbose_name="Collection Permission: Explicit?")
    gcp_comment = models.BooleanField(verbose_name="Collection Permission: Can Comment?")
    gcp_profile = models.UUIDField(verbose_name="Collection Permission: Source Profile")
    gcp_community = models.UUIDField(verbose_name="Collection Permission: Source Community")
    gc_id = models.BooleanField(verbose_name="Gallery Collection ID")
    gc_label = models.BooleanField(verbose_name="Gallery Collection Label")
    gc_created = models.DateTimeField(verbose_name="Gallery Collection Created")
    gc_updated = models.DateTimeField(verbose_name="Gallery Collection Updated")
    gc_items = models.IntegerField(verbose_name="Gallery Collection Items")
    gc_likes = models.IntegerField(verbose_name="Gallery Collection Likes")
    gc_views = models.IntegerField(verbose_name="Gallery Collection Views")
    gc_shares = models.IntegerField(verbose_name="Gallery Collection Shares")
    gc_comments = models.IntegerField(verbose_name="Gallery Collection Comments")
    gc_uuid = models.UUIDField(verbose_name="Gallery Collection UUID")
    gci_hash = models.CharField(verbose_name="Gallery Item Hash",max_length=200)
    gci_title = models.CharField(verbose_name="Gallery Item Title",max_length=200)
    gci_descr = models.CharField(verbose_name="Gallery Item Description",max_length=200)
    gci_details = models.CharField(verbose_name="Gallery Item Details Style",max_length=200)
    gci_hash = models.CharField(verbose_name="Gallery Item Hash",max_length=200)
    gci_created = models.DateTimeField(verbose_name="Gallery Item Created")
    gci_updated = models.DateTimeField(verbose_name="Gallery Item Updated")
    gci_files = models.IntegerField(verbose_name="Gallery Item Files")
    gci_views = models.IntegerField(verbose_name="Gallery Item Views")
    #gci_items = models.IntegerField(verbose_name="Gallery Item Items")
    gci_likes = models.IntegerField(verbose_name="Gallery Item Likes")
    gci_shares = models.IntegerField(verbose_name="Gallery Item Shares")
    gci_comments = models.IntegerField(verbose_name="Gallery Item Comments")
    gci_nsfw = models.BooleanField(verbose_name="Collection Item: NSFW?")
    gci_plugin = models.JSONField(verbose_name="Gallery Item Plguin")
    gci_plugin_data = models.JSONField(verbose_name="Gallery Item Plguin JSON Data")
    gci_thumbnail = models.BooleanField(verbose_name="Collection Item: Thumbnail?")
    gci_processed = models.BooleanField(verbose_name="Collection Item: Processed?")
    gci_uuid = models.UUIDField(verbose_name="Gallery Item UUID")
    gci_configured = models.BooleanField(verbose_name="Gallery Item Configured")
    gci_active = models.BooleanField(verbose_name="Gallery Item Active")
    gci_archived = models.BooleanField(verbose_name="Gallery Item Archived")
    gci_frozen = models.BooleanField(verbose_name="Gallery Item Frozen")
    gci_downloads = models.BooleanField(verbose_name="Gallery Item Downloads")
    gci_profile = models.UUIDField(verbose_name="Gallery Item Profile")
    gci_sizing = models.IntegerField(verbose_name="Gallery Item Sizing")
    gci_style = models.CharField(verbose_name="Gallery Item Style",max_length=200)
    gci_rating = models.CharField(verbose_name="Gallery Item Rating",max_length=200)
    gif_name = models.CharField(verbose_name="Gallery File Name",max_length=200)
    gif_hash = models.CharField(verbose_name="Gallery File Hash",max_length=200)
    gif_id = models.IntegerField(verbose_name="Gallery File ID")
    gif_data = models.CharField(verbose_name="Gallery File Data",max_length=200)
    gif_created = models.DateTimeField(verbose_name="Gallery File Created")
    gif_updated = models.DateTimeField(verbose_name="Gallery File Updated")
    gif_meta = models.JSONField(verbose_name="Gallery File Metadata")
    gif_bindata = models.BinaryField(verbose_name="Gallery File Binary Data")
    gif_jsondata = models.JSONField(verbose_name="Gallery File Json data")
    gif_thumbnail = models.BooleanField(verbose_name="Gallery File: is thumbnail?")
    gif_size = models.IntegerField(verbose_name="Gallery File Size")
    gif_type = models.CharField(verbose_name="Gallery File Type",max_length=200)
    gif_original = models.BooleanField(verbose_name="Gallery File: Original?")
    gif_item = models.UUIDField(verbose_name="Gallery File Item UUID")
    profile_name = models.CharField(verbose_name="Profile Name",max_length=200)
    profile_pronouns = models.CharField(verbose_name="Profile Pronouns",max_length=200)
    profile_avatar = models.CharField(verbose_name="Profile Avtar",max_length=200)
    profile_slug = models.CharField(verbose_name="Profile Slug",max_length=200)
    profile_uuid = models.CharField(verbose_name="Profile UUID",max_length=200)
    collection = models.ForeignKey(GalleryCollection,verbose_name='Collection',on_delete=models.CASCADE)
    item = models.ForeignKey(GalleryItem,verbose_name='File',on_delete=models.CASCADE)
    file = models.ForeignKey(GalleryItemFile,verbose_name='File',on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name="Profile",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    def __str__(self):
        return f"Gallery Permissions Item: collection.item.file: {self.collection.label}.{self.item.item_hash}.{self.file.name}"
    class Meta:
        managed = False
        db_table = 'gallery_itemsbycollectionpermission'


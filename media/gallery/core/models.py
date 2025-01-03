from django.db import models
from django.contrib import admin
from communities.profiles.models import Profile
from communities.community.models import Community
from communities.group.models import Group
from content_manager.keywords.models import Keyword
from content_manager.categories.models import Category
import uuid,json

# Create your models here.

class GalleryPlugins(models.Model):
    class Meta:
        db_table =  "media_gallery_core_plugins"
    app = models.CharField(verbose_name="Application/plugin name",unique=True)
    settings_model = models.CharField(verbose_name="Application/plugin Settings Model")
    name = models.CharField(verbose_name="Plugin's Human-readable name",null=True)
    descr = models.CharField(verbose_name="Plugin's Human-friendly description",blank=True,null=True)
    author = models.CharField(verbose_name="Plugin's Author",null=True)
    version = models.CharField(verbose_name="Plugin's Version",default='0.0.0')
    url = models.CharField(verbose_name="Plugin's URL: Homepage",blank=True)
    repo = models.CharField(verbose_name="Plugin's URL: Repository",null=True)
    icon = models.CharField(verbose_name="Plugin's Icon for Sidebars",null=True)
    installed = models.DateTimeField(auto_now_add=True,verbose_name="Plugin Installed Date")
    def __str__(self):
        return f"Gallery Plugin: {self.app}  - {self.name} (v. {self.version})"
@admin.register(GalleryPlugins)
class GalleryPluginsAdmin(admin.ModelAdmin):
    pass
class GalleryPluginVersionHistory(models.Model):
    class Meta:
        db_table =  "media_gallery_core_plugin_version_history"
    app = models.ForeignKey(GalleryPlugins,on_delete=models.CASCADE)
    old_version = models.CharField(verbose_name="Plugin's Old Version")
    version = models.CharField(verbose_name="Plugin's Current Version")
    updated = models.DateTimeField(auto_now_add=True,verbose_name="Plugin Installed Date")
    def __str__(self):
        return f"Gallery Plugin: {self.app} Version Update History: {self.old_version}->{self.version}"
@admin.register(GalleryPluginVersionHistory)
class GalleryPluginVersionHistoryAdmin(admin.ModelAdmin):
    pass

class GalleryCoreSettings(models.Model):
    class Meta:
        db_table =  "media_gallery_core_settings"
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True,blank=True,unique=True)
    enable_gallery = models.BooleanField(verbose_name="Enable Gallery Module",default=False,help_text="Enable/Disable the Gallery module globally for the community. (This does not delete any files that already exist if disabled.)")
    enable_stream_integration = models.BooleanField(verbose_name="Enable Gallery<->Stream Integration",default=True,help_text="Enabling Gallery/Stream integration will enable users to automatically publish new gallery content to streams.")
    enable_rss_publishing = models.BooleanField(verbose_name="Enable Gallery RSS Publishing",default=True,help_text="Enabling Gallery RSS publishing allows users to create RSS stream(s) to broadcast new gallery content.")
    enable_fed_publishing = models.BooleanField(verbose_name="Enable Gallery Federation Publishing",default=True,help_text="Enabling Gallery Federation will enable users to Federate their galleries.")
    enable_group_galleries = models.BooleanField(verbose_name="Enable Galleries for User Groups",default=True,help_text="Allow Groups to create and own galleries?")
    enable_metrics = models.BooleanField(verbose_name="Enable Gallery Metrics",default=True,help_text="Enable the Gallery Metrics module to collect insight on traffic and usage patterns (and share it with the authors.)")
    gallery_max_filesize = models.IntegerField(verbose_name="Maximum File Size in MB",default=25,help_text="The absolute maximum file size allowed in the Gallery in megabytes. All modules are limited by this parameter.")
    enabled_plugins = models.ManyToManyField(GalleryPlugins,verbose_name="Enabled Gallery Plugins:")
    def __str__(self):
        return f"Gallery Core Settings for Community: {self.community}"

@admin.register(GalleryCoreSettings)
class GalleryCoreSettingsAdmin(admin.ModelAdmin):
    pass

class GalleryType(models.Model):
    class Meta:
        db_table =  "media_gallery_core_type"
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
    class Meta:
        db_table =  "media_gallery_core_artwork_cat"
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
    class Meta:
        db_table =  "media_gallery_core_cat_groups"
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
    class Meta:
        db_table =  "media_gallery_core_cat_group_object"
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
    class Meta:
        db_table =  "media_gallery_core_item_types"
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
    class Meta:
        db_table =  "media_gallery_core_item"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    item_hash = models.TextField(max_length=200,verbose_name='Item Hash')
    title = models.TextField(max_length=200,verbose_name='Item Title')
    profile = models.ForeignKey(Profile,verbose_name='Item Owner',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,verbose_name='Item Category',on_delete=models.CASCADE)
    sizing = models.IntegerField(verbose_name='Sizing Hint',default=0)
    nsfw = models.CharField(verbose_name="Item NSFW Flag",default=False,max_length=10)
    en_comments = models.BooleanField(verbose_name="Item Comments Enabled Flag",default=True)
    en_sharing = models.BooleanField(verbose_name="Item Sharing Enabled Flag",default=True)
    en_download = models.BooleanField(verbose_name="Item Download Enabled Flag",default=True)
    details = models.CharField(verbose_name="Item Details Flags",default=False,max_length=10)
    style = models.CharField(verbose_name="Item Style Flag",default=False,max_length=10)
    rating = models.CharField(verbose_name="Item Rating",default=False,max_length=10)
    descr = models.TextField(max_length=200,verbose_name='Item Description')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Item Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='tem Updated')
    files = models.IntegerField(verbose_name='File Count',default=0)
    plugin = models.TextField(verbose_name="Item Plugin",default='',null=True)
    detail_style = models.TextField(verbose_name="Item Detail Style",default='b')
    sizing_hint = models.TextField(verbose_name="Item Sizing Hint",default='1')
    display_details = models.TextField(verbose_name="Item Display Details",default='t')
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
    class Meta:
        db_table =  "media_gallery_core_item_file"
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
        if self.thumbnail is False and self.original is False:
            return f"Gallery Item Display File: {self.name}"
        elif self.original is True:
            return f"Gallery Item Original File: {self.name}"
        else:
            return f"Gallery Item File: {self.name}"

@admin.register(GalleryItemFile)
class GalleryItemFileAdmin(admin.ModelAdmin):
    pass

class GalleryCollection(models.Model):
    class Meta:
        db_table =  "media_gallery_core_collection"
        unique_together = ['collection_id','owner']
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    collection_id = models.TextField(max_length=200,verbose_name='Collection ID')
    label = models.TextField(max_length=200,verbose_name='Collection Label')
    owner = models.ForeignKey(Profile,verbose_name="Collection Owner",on_delete=models.RESTRICT)
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
    class Meta:
        db_table =  "media_gallery_core_collection_items"
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
    class Meta:
        db_table =  "media_gallery_core_item_category"
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
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
    class Meta:
        db_table =  "media_gallery_core_item_keyword"
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,verbose_name='keyword',on_delete=models.RESTRICT)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Gallery Keyword: {self.item.uuid} -> Keyword: {self.keyword.keyword}"
@admin.register(GalleryItemKeyword)
class GalleryItemKeywordAdmin(admin.ModelAdmin):
    pass

class GalleryItemComments(models.Model):
    class Meta:
        db_table =  "media_gallery_core_item_comments"
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
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
    class Meta:
        db_table =  "media_gallery_core_collection_permission"
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
    class Meta:
        db_table =  "media_gallery_core_temp_file"
    name = models.TextField(verbose_name='File Name')
    profile = models.ForeignKey(Profile,verbose_name='Profile',on_delete=models.RESTRICT,null=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    file_size = models.FloatField(verbose_name='File Size',default=0,blank=True,null=True)
    type = models.TextField(verbose_name='File Type',blank=True,null=True)
    thumbnail = models.TextField(verbose_name='File Thumbnail',blank=True,null=True)
    plugin = models.TextField(verbose_name='File Plugin',blank=True,null=True)
    path = models.TextField(verbose_name='File Path',blank=True,null=True)
    data = models.TextField(verbose_name='File Text Data',blank=True,null=True)
    bindata = models.BinaryField(verbose_name='File Bindata',blank=True,null=True)
    jsondata = models.JSONField(verbose_name='File JSONData',blank=True,null=True)
    userdata = models.JSONField(verbose_name='File User Review JSONData',default={})
    meta = models.JSONField(verbose_name='File Metadata',blank=True,null=True,default={})
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

class GalleryTempFileThumb(models.Model):
    class Meta:
        db_table =  "media_gallery_core_temp_file_thumb"
    file = models.ForeignKey(GalleryTempFile,verbose_name='Item',on_delete=models.CASCADE)
    path = models.TextField(verbose_name='File Path',blank=True,null=True)
    file_size = models.FloatField(verbose_name='File Size',default=0)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Gallery Item Temporary File Thumbnail: {self.file.name} @ {self.path}"
    def get_meta_json(self):
        return str(json.dumps(self.meta))
@admin.register(GalleryTempFileThumb)
class GalleryTempFileThumbAdmin(admin.ModelAdmin):
    pass

class GalleryTempFileCollections(models.Model):
    class Meta:
        db_table =  "media_gallery_core_temp_file_collections"
    collection = models.ForeignKey(GalleryCollection,verbose_name='Collection',on_delete=models.CASCADE)
    file = models.ForeignKey(GalleryTempFile,verbose_name='Item',on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)


class GalleryTempFileKeywords(models.Model):
    class Meta:
        db_table =  "media_gallery_core_temp_file_keywords"
    file = models.ForeignKey(GalleryTempFile,verbose_name='Temp File',on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,verbose_name='keyword',on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)


class GalleryFavourite(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True,blank=True)
    profile = models.ForeignKey(Profile,verbose_name='Item',on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False,null=True)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    flagged = models.BooleanField(verbose_name="FLAGGED",default=False)
    class Meta:
        db_table =  "media_gallery_core_favourite"
        constraints = [
            models.UniqueConstraint(fields=['item', 'profile','community'], name='unique_favourite')
        ]
    def __str__(self):
        return f"Gallery Favourite: {self.profile.profile_id} fav'd {self.item.title}"

@admin.register(GalleryFavourite)
class GalleryFavouriteAdmin(admin.ModelAdmin):
    pass

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
        db_table = 'media_gallery_core_collection_permission_view'



class GalleryItemsByFavourites(models.Model):

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
    gif_profile = models.UUIDField(verbose_name="Gallery Item Profile")
    gci_sizing = models.IntegerField(verbose_name="Gallery Item Sizing")
    gci_style = models.CharField(verbose_name="Gallery Item Style",max_length=200)
    gci_rating = models.CharField(verbose_name="Gallery Item Rating",max_length=200)
    gif_name = models.CharField(verbose_name="Gallery File Name",max_length=200)
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
    gif_profile = models.UUIDField(verbose_name="Gallery Favorite Profile UUID")
    gc_uuid = models.UUIDField(verbose_name="Gallery Collection UUID")
    collection_id = models.UUIDField(verbose_name="Gallery Collection UUID")
    gal_path = models.CharField(verbose_name="Gallery Path",max_length=200)
    profile_name = models.CharField(verbose_name="Profile Name",max_length=200)
    profile_pronouns = models.CharField(verbose_name="Profile Pronouns",max_length=200)
    profile_avatar = models.CharField(verbose_name="Profile Avtar",max_length=200)
    profile_slug = models.CharField(verbose_name="Profile Slug",max_length=200)
    profile_uuid = models.CharField(verbose_name="Profile UUID",max_length=200)
    item = models.ForeignKey(GalleryItem,verbose_name='File',on_delete=models.CASCADE)
    file = models.ForeignKey(GalleryItemFile,verbose_name='File',on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name="Profile",on_delete=models.CASCADE)
    def __str__(self):
        return f"Gallery Favourite Item: item.file in item.id: {self.item.item_hash}.{self.gci_uuid} for profile {self.profile_slug}"
    class Meta:
        managed = False
        db_table = 'media_gallery_core_items_by_favourite_view'


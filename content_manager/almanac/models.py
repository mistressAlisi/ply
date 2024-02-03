from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from martor.models import MartorField
from communities.community.models import Community
import uuid

# Create your models here.
from communities.profiles.models import Profile
from core.dynapages import models as dynamodels


class AlmanacPage(models.Model):
    class Meta:
        db_table ="content_manager_almanac_page"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    page_id = models.TextField(max_length=200,verbose_name='Page ID',unique=True)
    title = models.TextField(max_length=200,verbose_name='Page Title')
    owner = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.CASCADE)
    creator = models.ForeignKey(Profile,verbose_name = "Creator Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Page Created')
    dynaPage = models.ForeignKey(dynamodels.Templates,on_delete=models.RESTRICT,blank=True,null=True,related_name='+',verbose_name="DynaPage Template")
    updated = models.DateTimeField(verbose_name='Page Updated',auto_now_add=True)
    introduction = models.TextField(verbose_name='Page Intro')
    avatar = models.TextField(verbose_name='Avatar URL',null=True,blank=True) 
    posts = models.IntegerField(verbose_name='Post Count',default=0)
    views = models.IntegerField(verbose_name='View Count',default=0)
    nodes = models.IntegerField(verbose_name='Node Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"Page: \"{self.title}\",  owner: {self.owner}, creator: {self.creator}"
@admin.register(AlmanacPage)
class PageAdmin(admin.ModelAdmin):
    pass

class AlmanacPageText(models.Model):
    class Meta:
        db_table ="content_manager_almanac_page_text"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    page = models.ForeignKey(AlmanacPage,verbose_name = "AlmanacPage",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Page Text Created')
    updated = models.DateTimeField(verbose_name='Page Updated',auto_now_add=True)
    language = models.TextField(max_length=5,verbose_name='Page Language',default='en-US')
    page_contents = MartorField(verbose_name='Page Contents')
    current = models.BooleanField(verbose_name="current FLAG",default=False)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    def __str__(self):
        return f"Almanac Page Text for Almanac Page \"{self.page.page_id}\" created on {self.created}: Current: {self.current}"
@admin.register(AlmanacPageText)
class PageTextAdmin(admin.ModelAdmin):
    pass


class AlmanacMenuCategory(models.Model):
    class Meta:
        db_table ="content_manager_almanac_menu_category"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    category_id = models.TextField(max_length=200,verbose_name='MenuCat ID',unique=True)
    icon = models.TextField(max_length=200,verbose_name='MenuCat Icon')
    title = models.TextField(max_length=200,verbose_name='MenuCat Title')
    order = models.IntegerField(verbose_name='Order Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"MenuCat: \"{self.name}\""
@admin.register(AlmanacMenuCategory)
class AlmanacMenuCategoryAdmin(admin.ModelAdmin):
    pass

class AlmanacMenuCategoryEntry(models.Model):
    class Meta:
        db_table ="content_manager_almanac_menu_category_entry"
    category = models.ForeignKey(AlmanacMenuCategory,verbose_name = "AlmanacMenu Category",on_delete=models.CASCADE)
    page = models.ForeignKey(AlmanacPage,verbose_name = "AlmanacPage",on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Order Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"MenuCat Entry: Menu \"{self.name}\""
@admin.register(AlmanacMenuCategoryEntry)
class AlmanacMenuCategoryEntryAdmin(admin.ModelAdmin):
    pass


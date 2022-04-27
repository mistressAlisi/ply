from django.db import models
from django.contrib import admin
from profiles.models import Profile
from django.contrib.auth.models import User
from group.models import Group
from gallery.models import GalleryItem
from community.models import Community
import uuid
# Create your models here.

class UserDataTotals(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Billing Created')
    updated = models.DateTimeField(verbose_name='Billing Updated',auto_now_add=True)
    period_start = models.DateTimeField(auto_now_add=True,verbose_name='Billing Period Start')
    period_end = models.DateTimeField(verbose_name='Billing Period End',auto_now_add=True)
    category = models.TextField(verbose_name='Billing Category')
    category_items = models.IntegerField(verbose_name='Billing category items',default=0)
    category_bytes = models.FloatField(verbose_name='Billing category bytes',default=0)
    category_xfer_bytes = models.FloatField(verbose_name='Billing category transferred bytes',default=0)
    def __str__(self):
        return f"User Data Totals User: {self.user.name} From: {self.period_start} to {self.period_end}. Category: {self.category} with {self.category_items} items in total, {self.category_bytes/1024} kB in total."
@admin.register(UserDataTotals)
class UserDataTotalsAdmin(admin.ModelAdmin):
    pass


class UserDataEntry(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Billing Created')
    updated = models.DateTimeField(verbose_name='Billing Updated',auto_now_add=True)
    category = models.TextField(verbose_name='Billing Category')
    reference = models.TextField(verbose_name='Billing Reference')
    bytes = models.FloatField(verbose_name='Billing category bytes',default=0)
    xfer_bytes = models.FloatField(verbose_name='Billing category transferred bytes',default=0)
    def __str__(self):
        return f"User Data Billing Entry for User: {self.user.username} . Category: {self.category}, {self.bytes/1024} kB. Xfer: {self.xfer_bytes/1024} kB."
@admin.register(UserDataEntry)
class UserDataEntryAdmin(admin.ModelAdmin):
    pass

    
class GroupDataTotals(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    group = models.ForeignKey(Group,verbose_name = "Group",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Billing Created')
    updated = models.DateTimeField(verbose_name='Billing Updated',auto_now_add=True)
    period_start = models.DateTimeField(auto_now_add=True,verbose_name='Billing Period Start')
    period_end = models.DateTimeField(verbose_name='Billing Period End',auto_now_add=True)
    category = models.TextField(verbose_name='Billing Category')
    category_items = models.IntegerField(verbose_name='Billing category items',default=0)
    category_bytes = models.FloatField(verbose_name='Billing category bytes',default=0)
    category_xfer_bytes = models.FloatField(verbose_name='Billing category transferred bytes',default=0)
    def __str__(self):
        return f"Group Data Totals Group: {self.uuid.name} From: {self.period_start} to {self.period_end}. Category: {self.category} with {self.category_items} items in total, {self.category_bytes/1024} kB in total."
@admin.register(GroupDataTotals)
class GroupDataTotalsAdmin(admin.ModelAdmin):
    pass
        


class GalleryItemHit(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    type = models.TextField(verbose_name='Item Hit Type',db_index=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    remote_addr = models.GenericIPAddressField(blank=True, null=True, verbose_name=("remote address"))
    user_agent = models.TextField(verbose_name='Hit User Agent',db_index=True,blank=True)
    profile = models.ForeignKey(Profile,verbose_name='Item Viewed by Profile',on_delete=models.CASCADE,blank=True)
    group = models.ForeignKey(Group,verbose_name = "Item viewed by member of group",on_delete=models.CASCADE,blank=True)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    def __str__(self):
        return f"Gallery Item Hit: {self.item.uuid} at: {self.created} (IP: {self.remote_addr}) (X-UA: {self.user_agent})"
@admin.register(GalleryItemHit)
class GalleryItemHitAdmin(admin.ModelAdmin):
    pass
  
class GalleryItemHitTotals(models.Model):
    item = models.ForeignKey(GalleryItem,verbose_name='Item',on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    type = models.TextField(verbose_name='Hit Type',db_index=True)
    totals = models.IntegerField(verbose_name='Total views',default=0)
    def __str__(self):
        return f"Gallery Item Hit Totals: {self.item.uuid} for: {self.community.uuid}"
@admin.register(GalleryItemHitTotals)
class GalleryItemHitTotalsAdmin(admin.ModelAdmin):
    pass
  
class ProfilePageHit(models.Model):
    profile = models.ForeignKey(Profile,verbose_name='Parent',on_delete=models.CASCADE,related_name="+")
    type = models.TextField(verbose_name='Hit Type',db_index=True)
    updated = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    visitor = models.ForeignKey(Profile,verbose_name='Viewed by Profile',on_delete=models.CASCADE,related_name="+")
    group = models.ForeignKey(Group,verbose_name = "viewed by member of group",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    def __str__(self):
        return f"Profile Page Hit: {self.visitor.uuid} for: {self.profile.uuid}'s profile"
@admin.register(ProfilePageHit)
class ProfilePageHitAdmin(admin.ModelAdmin):
    pass
    
class ProfilePageHitTotals(models.Model):
    profile = models.ForeignKey(Profile,verbose_name='Parent',on_delete=models.CASCADE,related_name="+")
    type = models.TextField(verbose_name='Hit Type',db_index=True)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)    
    totals = models.IntegerField(verbose_name='Total views',default=0)
    def __str__(self):
        return f"Profile Item Hit Totals: {self.profile.uuid} for: {self.community.uuid}"
@admin.register(ProfilePageHitTotals)
class ProfilePageHitTotalsAdmin(admin.ModelAdmin):
    pass

class GroupPageHit(models.Model):
    group = models.ForeignKey(Group,verbose_name='Parent',on_delete=models.CASCADE)
    type = models.TextField(verbose_name='Hit Type',db_index=True)
    updated = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    visistor = models.ForeignKey(Profile,verbose_name='Viewed by Profile',on_delete=models.CASCADE)
    group = models.ForeignKey(Group,verbose_name = "viewed by member of group",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)
    def __str__(self):
        return f"Group Page Hit: {self.visitor.uuid} group: {self.group.uuid}"
@admin.register(GroupPageHit)
class GroupPageHitAdmin(admin.ModelAdmin):
    pass


class GroupPageHitTotals(models.Model):
    group = models.ForeignKey(Group,verbose_name='Parent',on_delete=models.CASCADE)
    type = models.TextField(verbose_name='Hit Type',db_index=True)
    community = models.ForeignKey(Community,verbose_name = "Community",on_delete=models.RESTRICT)    
    totals = models.IntegerField(verbose_name='Total views',default=0)
    def __str__(self):
        return f"Group Page Hit Totals: {self.group.uuid} for: {self.community.uuid}"
@admin.register(GroupPageHitTotals)
class GroupPageHitTotalsAdmin(admin.ModelAdmin):
    pass

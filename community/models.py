from django.db import models
from django.contrib import admin
import uuid


# PLY
from profiles.models import Profile
from group.models import Group
from dynapages.models import Page
# Create your models here.
class Community(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    hash = models.TextField(max_length=200,verbose_name='Community Hash')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    updated = models.DateTimeField(verbose_name='Profile Updated',auto_now_add=True)
    dynapage = models.ForeignKey(Page,on_delete=models.RESTRICT,blank=True,null=True)
    name = models.TextField(verbose_name='Name')
    action_call_cover = models.TextField(verbose_name='Action Call for Cover page')
    introduction = models.TextField(verbose_name='Introduction')
    tagline = models.TextField(verbose_name='Tagline',null=True)
    avatar = models.TextField(verbose_name='Avatar',null=True)
    posts = models.IntegerField(verbose_name='Post Count',default=0)
    profile = models.IntegerField(verbose_name='Profile Count',default=0)
    group = models.IntegerField(verbose_name='Group Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    restricted = models.BooleanField(verbose_name="Restricted Join Mode FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    backgroundItem = models.ForeignKey('gallery.GalleryItem',blank=True,null=True,on_delete=models.RESTRICT)
    def __str__(self):
        return f"Community: {self.name}, hash: {self.hash}"
    
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass  

class VHost(models.Model):
    community = models.ForeignKey(Community,verbose_name="Community to Apply to VHOST",on_delete=models.CASCADE,default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='VHost Created')
    updated = models.DateTimeField(verbose_name='VHost Updated',auto_now_add=True)
    hostname = models.TextField(max_length=200,null=True,verbose_name='VHost Hostname')
    ipaddr = models.GenericIPAddressField(null=True,verbose_name='VHost IP address')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    restricted = models.BooleanField(verbose_name="Restricted Joining FLAG",default=False)
    def __str__(self):
        return f"VHost - Hostname: {self.hostname}. IPAddr: {self.ipaddr}: Community: {self.community.name}"
    
@admin.register(VHost)
class VHostAdmin(admin.ModelAdmin):
    pass  


class CommunityProfile(models.Model):
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "User",on_delete=models.RESTRICT,null=True)
    joined = models.DateTimeField(verbose_name='Joined')
    def __str__(self):
        return f"Community: {self.community.name}. Profile: {self.profile.name}. Joined: {self.joined}"
@admin.register(CommunityProfile)
class CommunityProfileAdmin(admin.ModelAdmin):
    pass  

class CommunityGroup(models.Model):
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    group = models.ForeignKey(Group,verbose_name = "Group",on_delete=models.RESTRICT,null=True)
    joined = models.DateTimeField(verbose_name='Joined')
    def __str__(self):
        return f"Community: {self.community.name}. Group: {self.group.name}. Joined: {self.joined}"
@admin.register(CommunityGroup)
class CommunityGroupAdmin(admin.ModelAdmin):
    pass  


class CommunityAdmins(models.Model):
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "User",on_delete=models.RESTRICT,null=True)
    joined = models.DateTimeField(verbose_name='Joined')
    active = models.BooleanField(verbose_name="Active FLAG",default=True)
    def __str__(self):
        return f"Community ADMIN: {self.community.name}. Profile: {self.profile.name}."
@admin.register(CommunityAdmins)
class CommunityAdminsAdmin(admin.ModelAdmin):
    pass  

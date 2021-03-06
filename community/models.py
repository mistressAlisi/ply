from django.db import models
from django.contrib import admin
import uuid
from django.contrib.auth.models import User

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

class ProfilePerCoummunityView(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community_uuid = models.UUIDField(verbose_name="Community UUID")
    profile_creator = models.IntegerField(verbose_name='Owner ID',default=0)
    joined = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Joined')
    community_name = models.TextField(verbose_name='Community Name')
    profile_created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    dynapage = models.ForeignKey(Page,on_delete=models.RESTRICT,blank=True,null=True)
    profile_updated = models.DateTimeField(verbose_name='Profile Updated',auto_now_add=True)
    last_seen = models.DateTimeField(verbose_name='Profile Last Seen Online',auto_now_add=True)
    age = models.TextField(verbose_name='Current Age',default=1,blank=True)
    name = models.TextField(verbose_name='Name')
    status = models.TextField(verbose_name='status',default="CITIZEN",blank=True)
    species = models.TextField(verbose_name='Species',default='Sentient')
    introduction = models.TextField(verbose_name='Profile Intro')
    level = models.TextField(verbose_name='Current Level',default=1)
    max_HP = models.TextField(verbose_name='Max HP',default=10)
    HP = models.TextField(verbose_name='Current HP',default=10)
    max_MP = models.TextField(verbose_name='Max MP',default=6)
    STUN = models.TextField(verbose_name='Current STUN',default=10)
    max_STUN = models.TextField(verbose_name='Max STUN',default=6)
    SHIELD = models.TextField(verbose_name='Current SHIELD',default=10)
    max_SHIELD = models.TextField(verbose_name='Max SHIELD',default=6)
    MP = models.TextField(verbose_name='Current MP',default=6)
    max_STA = models.TextField(verbose_name='Max STA',default=10)
    STA = models.TextField(verbose_name='Current STA',default=10)
    views = models.IntegerField(verbose_name='Post Count',default=0)
    slug = models.TextField(verbose_name='Slugified Name')
    pronouns = models.TextField(max_length=200,verbose_name='Pronouns')
    gender = models.TextField(max_length=200,verbose_name='Gender')
    avatar = models.TextField(verbose_name='Avatar URL',null=True,blank=True) 
    posts = models.IntegerField(verbose_name='Post Count',default=0)
    views = models.IntegerField(verbose_name='Post Count',default=0)
    nodes = models.IntegerField(verbose_name='Node Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    profile = models.ForeignKey(Profile,verbose_name="Profile",on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    creator = models.ForeignKey(User,verbose_name="User",on_delete=models.CASCADE)
    def __str__(self):
        return f"Profile {self.profile_id} as member of Community {self.name}"
    class Meta:
        managed = False
        db_table = 'community_profilepercommunityview'

# Followers Table:
class Follower(models.Model):
    source = models.ForeignKey(Profile,verbose_name = "Source Profile",on_delete=models.RESTRICT,related_name='+')
    dest = models.ForeignKey(Profile,verbose_name = "Dest Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Relationship Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"Follower: {self.source.uuid} -follows-> {self.dest.uuid} in community: {self.community.uuid}"
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass

# Friends Table:
class Friend(models.Model):
    friend1 = models.ForeignKey(Profile,verbose_name = "Friend 1 Profile",on_delete=models.RESTRICT,related_name='+')
    friend2 = models.ForeignKey(Profile,verbose_name = "Friend 2 Profile",on_delete=models.RESTRICT,related_name='+')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Request Created')
    approved = models.DateTimeField(verbose_name="Approved?",null=True)
    approved_flag = models.BooleanField(verbose_name="Approved FLAG",default=False)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"Friends: {self.friend1.uuid} <-> {self.friend2.uuid}  in community: {self.community.uuid}"
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass

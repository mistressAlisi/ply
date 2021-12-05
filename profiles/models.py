from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Profile(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    profile_id = models.TextField(max_length=200,verbose_name='Profile ID')
    creator = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    updated = models.DateTimeField(verbose_name='Profile Updated',auto_now_add=True)
    name = models.TextField(verbose_name='Name')
    slug = models.TextField(verbose_name='Slugified Name')
    pronouns = models.TextField(max_length=200,verbose_name='Pronouns')
    avatar = models.TextField(verbose_name='Avatar URL',null=True,blank=True)
    posts = models.IntegerField(verbose_name='Post Count',default=0)
    views = models.IntegerField(verbose_name='Post Count',default=0)
    nodes = models.IntegerField(verbose_name='Node Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        
        return f"Profile ID: {self.name} from user: {self.creator.username}"
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    
# Followers Table:
class Follower(models.Model):
    source = models.ForeignKey('Profile',verbose_name = "Source Profile",on_delete=models.RESTRICT,related_name='+')
    dest = models.ForeignKey('Profile',verbose_name = "Dest Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Relationship Created')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass

# Friends Table:
class Friend(models.Model):
    friend1 = models.ForeignKey('Profile',verbose_name = "Friend 1 Profile",on_delete=models.RESTRICT,related_name='+')
    friend2 = models.ForeignKey('Profile',verbose_name = "Friend 2 Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Request Created')
    approved = models.DateTimeField(verbose_name="Approved?",null=True)
    approved_flag = models.BooleanField(verbose_name="Approved FLAG",default=False)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
    
# The ticket system is used to keep track of support / behaviour requests on behalf of bad profiles or actors. Or in case a user needs support:
class TicketType(models.Model):
    type_id = models.TextField(max_length=200,verbose_name='Type ID')
    label = models.TextField(max_length=200,verbose_name='Type Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Type Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Type Updated')
    tickets = models.IntegerField(verbose_name='Ticket Count',null=True,blank=True,default=0)
    def __str__(self):
        return f"Ticket Type: {self.label}"
    
@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    pass


class Ticket(models.Model):
    type = models.ForeignKey(TicketType,verbose_name = 'Ticket Type',on_delete=models.RESTRICT)
    profile = models.ForeignKey(Profile,verbose_name = "User",on_delete=models.RESTRICT,null=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Ticket Created')
    updated = models.DateTimeField(verbose_name='Ticket Updated',auto_now_add=True)
    opened = models.DateTimeField(verbose_name='Ticket Initially Opened')
    responded = models.DateTimeField(verbose_name='Ticket Initial Response')
    notes = models.TextField(verbose_name='Ticket Notes',null=True)
    reference = models.TextField(verbose_name='Ticket Reference',null=True)
    contributors = models.TextField(verbose_name='Ticket Contributors',null=True)
    fix = models.TextField(verbose_name='Ticket Fix',null=True)
    archived = models.BooleanField(verbose_name="Ticket Archived",default=False)
    def __str__(self):
        return f"Ticket: {self.id} "
    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


class ProfilePermission(models.Model):
    profile = models.ForeignKey(Profile,verbose_name='Profile',on_delete=models.RESTRICT,related_name="+")
    visitor = models.ForeignKey(Profile,verbose_name='Visitor',on_delete=models.RESTRICT,null=True,related_name="+")
    group = models.ForeignKey('group.Group',verbose_name='Group',on_delete=models.RESTRICT,null=True)
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
        return f"Permissions for Profile: {profile.label}, Visitor: {visitor.name}, group: {group.name}"
    
@admin.register(ProfilePermission)
class ProfilePermissionAdmin(admin.ModelAdmin):
    pass
     

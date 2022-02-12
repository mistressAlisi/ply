from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from profiles.models import Profile
from keywords.models import Keyword
from dynapages.models import Page
import uuid
# Create your models here.

class Group(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    creator = models.ForeignKey(User,verbose_name = "User (Creator)",on_delete=models.CASCADE)
    creator_profile = models.ForeignKey(Profile,verbose_name = "Profile (Creator)",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Group Created')
    updated = models.DateTimeField(verbose_name='Profile Updated',auto_now_add=True)
    dynapage = models.ForeignKey(Page,on_delete=models.RESTRICT,blank=True,null=True)
    name = models.TextField(verbose_name='Name')
    impressum = models.TextField(verbose_name='Impressum')
    avatar = models.TextField(verbose_name='Avatar URL',null=True)
    posts = models.IntegerField(verbose_name='Post Count',default=0)
    views = models.IntegerField(verbose_name='Post Count',default=0)
    members = models.IntegerField(verbose_name='Member Count',default=0)
    nodes = models.IntegerField(verbose_name='Node Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"Group Name: {self.name}. Created by user: {self.creator.username}/{self.creator_profile.name}"
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
    

class GroupKeywords(models.Model):
    group = models.ForeignKey(Group,verbose_name='Groups',on_delete=models.RESTRICT)
    keyword = models.ForeignKey(Keyword,verbose_name='keyword',on_delete=models.RESTRICT)
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Group Keyword: {self.group.uuid} Keyword: {self.keyword}."
@admin.register(GroupKeywords)
class GroupKeywordsAdmin(admin.ModelAdmin):
    pass


class GroupTitle(models.Model):
    group = models.ForeignKey(Group,verbose_name='Group',on_delete=models.RESTRICT)
    title = models.TextField(max_length=200,verbose_name='Title')
    order = models.IntegerField(verbose_name='Order Column',default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Group Title: {self.title} for group: {self.group.name}."
@admin.register(GroupTitle)
class GroupTitleAdmin(admin.ModelAdmin):
    pass


class GroupMember(models.Model):
    group = models.ForeignKey(Group,verbose_name='Group',on_delete=models.RESTRICT)
    title = models.ForeignKey(GroupTitle,verbose_name='Group Title',on_delete=models.RESTRICT)
    profile = models.ForeignKey(Profile,verbose_name='Profile',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    primary = models.BooleanField(verbose_name="Primary FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Group Member: {self.profile.name} Group: {self.group.name}. Title: {self.title.title}"
@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    pass

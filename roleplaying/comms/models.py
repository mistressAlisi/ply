from django.db import models
from django.contrib import admin
from communities.profiles.models import Profile
# Create your models here.
# Notifications Table:
class Notification(models.Model):
    class Meta:
        db_table ="roleplaying_comms_notifications"
    source = models.ForeignKey(Profile,verbose_name = "Source Profile",on_delete=models.RESTRICT,related_name='+')
    dest = models.ForeignKey(Profile,verbose_name = "Dest Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Notification Created')
    recieved = models.DateTimeField(null=True,editable=False,verbose_name='Notification Recieved')
    opened = models.DateTimeField(null=True,editable=False,verbose_name='Notification Opened')
    read = models.DateTimeField(null=True,editable=False,verbose_name='Notification Read')
    type = models.TextField(max_length=200,verbose_name='Notification Type')
    label = models.TextField(verbose_name='Notification Label')
    slug = models.TextField(verbose_name='Notification Hash Slug')
    contents= models.TextField(verbose_name='Notification Contents')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass

class Message(models.Model):
    class Meta:
        db_table ="roleplaying_comms_message"
    source = models.ForeignKey(Profile,verbose_name = "Source Profile",on_delete=models.RESTRICT,related_name='+')
    dest = models.ForeignKey(Profile,verbose_name = "Dest Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Message Created')
    recieved = models.DateTimeField(null=True,editable=False,verbose_name='Message Recieved')
    opened = models.DateTimeField(null=True,editable=False,verbose_name='Message Opened')
    read = models.DateTimeField(null=True,editable=False,verbose_name='Message Read')
    type = models.TextField(max_length=200,verbose_name='Message Type')
    subject = models.TextField(verbose_name='Message subject')
    slug = models.TextField(verbose_name='Message Hash Slug')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

class MessageContents(models.Model):
    class Meta:
        db_table ="roleplaying_comms_message_contents"
    message = models.ForeignKey(Message,verbose_name = "Parent Message",on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(null=True,editable=False,verbose_name='Recieved')
    contents = models.TextField(verbose_name='Message Contents')
    attach = models.TextField(verbose_name='Message Attachments')
    
@admin.register(MessageContents)
class MessageContentsAdmin(admin.ModelAdmin):
    pass

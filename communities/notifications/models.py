from django.db import models
from django.contrib import admin
import uuid


# PLY
from communities.community.models import Community
from communities.profiles.models import Profile


# Notifications Table:
class Notification(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    source = models.ForeignKey(Profile,verbose_name = "Source Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Relationship Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    type = models.TextField(verbose_name='Notification Type')
    icon = models.TextField(verbose_name='Notification Icon',blank=True,null=True)
    contents_text = models.TextField(verbose_name='Notification Content: Text Type',blank=True,null=True)
    contents_json = models.JSONField(verbose_name='Notification Content: JSON Type',blank=True,null=True)
    contents_bin = models.BinaryField(verbose_name='Notification Content: Binary Type',blank=True,null=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)

    
    def __str__(self):
        return f"Notification: {self.uuid} -created by-> {self.source.uuid} in community: {self.community.uuid}"
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


# Notification Inbox Table:
class NotificationInbox(models.Model):
    notification = models.ForeignKey(Notification,verbose_name="Notification",on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile,verbose_name = "Recipient Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Notification Inbox Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    opened = models.DateTimeField(null=True,blank=True,verbose_name='Notification has been opened')
    replied = models.DateTimeField(null=True,blank=True,editable=False,verbose_name='Notification has been replied to')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    deleted = models.BooleanField(verbose_name="Deleted FLAG",default=False)
    deleted_on = models.DateTimeField(editable=False,verbose_name='Notification Inbox Deleted on',null=True)
    class Meta:
        unique_together = ('notification', 'community','recipient')
    
    def __str__(self):
        return f"Notification Inbox Index: Notification {self.notification.uuid} -in inbox for -> {self.recipient.uuid} in community: {self.community.uuid}"
@admin.register(NotificationInbox)
class NotificationInboxAdmin(admin.ModelAdmin):
    pass


# Profile Mentions Table:
class Mentions(models.Model):
    recipient = models.ForeignKey(Profile,verbose_name = "Recipient Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Mention Inbox Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    opened = models.DateTimeField(null=True,blank=True,verbose_name='Mention has been opened')
    replied = models.DateTimeField(null=True,blank=True,editable=False,verbose_name='Mention has been replied to')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    deleted = models.BooleanField(verbose_name="Deleted FLAG",default=False,null=True,blank=True,editable=True)
    deleted_on = models.DateTimeField(editable=False,verbose_name='Mention Inbox Deleted on',null=True,blank=True)
    type = models.TextField(verbose_name='Mention Type')
    contents_text = models.TextField(verbose_name='Mention Content: Text Type',blank=True,null=True)
    def __str__(self):
        return f"Mention Inbox Index: Mention for -> {self.recipient.uuid} in community: {self.community.uuid}: {self.type}"
@admin.register(Mentions)
class MentionInboxAdmin(admin.ModelAdmin):
    pass




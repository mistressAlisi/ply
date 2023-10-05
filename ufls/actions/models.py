import string
import uuid
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class StringKeyGenerator(object):
    def __init__(self, len=64):
        self.lenght = len
    def __call__(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(self.lenght))
    def salt(self):
        return ''.join(random.choice(string.ascii_uppercase) for x in range(self.lenght))

class Action(models.Model):
    id = models.CharField(unique=True, max_length=64, primary_key=True, default=StringKeyGenerator().__call__)
    subject = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    initiator = models.CharField(max_length=250, blank=True, null=True)
    dateEntered = models.DateTimeField(auto_now_add=True)
    actionUri = models.CharField(max_length=250, blank=True, null=True)
    read = models.BooleanField(default=False, help_text="Message was read by user but not acted on")
    completed = models.BooleanField(default=False, help_text="Message has been acted upon and should be archived as complete.")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('actions.Action', on_delete=models.SET_NULL, blank=True, null=True)
    settings = models.JSONField(default={"has_approve_decline": False, "has_delegate": False, "has_goto_resource": False})
    def isDelegated(self):
        if self.parent != None:
            return True
        return False
    def save(self, *args, **kwargs):
        super(Action, self).save(*args, **kwargs)
        salt = StringKeyGenerator().salt()
        async_to_sync(get_channel_layer().group_add)("inbox-%s" % (self.owner.pk), "trigger%s" % (salt))
        async_to_sync(get_channel_layer().group_send)("inbox-%s" % (self.owner.pk),
                                                      {'type': 'chat.message', 'text': {'action': 'refresh'}})
        async_to_sync(get_channel_layer().group_discard)("inbox-%s" % (self.owner.pk), "trigger%s" % (salt))
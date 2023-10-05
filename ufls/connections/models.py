from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.
class Application(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    postUrl = models.CharField(max_length=500, help_text="https URL to post return to with user account information. Should accept UFLS input.")
    allowedDomain = models.CharField(max_length=500, help_text="Domain used to validate access in Userland")
    enabled = models.BooleanField(default=False)
    staff_only = models.BooleanField(default=False, help_text="Only staff can access this application")
    show_on_app_list = models.BooleanField(default=False, help_text="Show this application on the application list")
    image = models.ImageField(blank=True, null=True)

class OTPKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4)
    application = models.ForeignKey('connections.Application', on_delete=models.CASCADE)

class StatusMessage(models.Model):
    dateExpires = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

class ReservationKey(models.Model):

    GROUPS = (
        ("Dealers", "Dealers"),
        ("Attendee Sponsors", "Attendee Sponsors"),
        ("Staff", "Staff"),
        ("Contractor", "Contractor"),
        ("Other", "Other")
    )

    key = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField()
    reservation = models.JSONField(default={}, blank=True, null=True)
    group = models.CharField(choices=GROUPS, max_length=100)
    sent = models.BooleanField(default=False, help_text="Have we sent them an e-mail yet?")
    def link(self):
        return "https://reservations.furrydelphia.org/invitation/%s/%s" % (self.email,self.key)
    def used(self):
        if(self.reservation != {}):
            return True
        return False
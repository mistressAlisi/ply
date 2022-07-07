import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
#PLY:
from community.models import Community
from profiles.models import Profile
# Create your models here.

# Mapping SLAgent to Ply Profile, 1 to n is supported of course.
class SLAgent(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = True)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    owner = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE,null=True)
    profile = models.ForeignKey(Profile,verbose_name = "Character Profile",on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Agent First seen')
    remote_addr = models.GenericIPAddressField(blank=True, null=True, verbose_name=("remote address"))
    last_view = models.DateTimeField(verbose_name="Last Viewed",null=True,auto_now_add=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    online = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"SL Agent Mapping {self.uuid} -maps to profile -> {self.profile.uuid} in community: {self.community.uuid}"

@admin.register(SLAgent)
class SLAgentAdmin(admin.ModelAdmin):
    pass


# Mapping SLAgent to Ply Community, 1 to n is supported of course.
class SLParcel(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = True)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Agent First seen')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    online = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"SL Parcel Mapping {self.uuid} -maps to community-> {self.community.uuid}"

@admin.register(SLParcel)
class SLParcelAdmin(admin.ModelAdmin):
    pass


# Mapping SLAgent to Ply Community, 1 to n is supported of course.
class SLParcelAgent(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['uuid'])
            ]
    parcel = models.ForeignKey(SLParcel,editable = True,verbose_name="Parcel",on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now_add=True,editable=True,verbose_name='Agent Last seen')
    uuid = models.UUIDField(default = uuid.uuid4,editable = True,verbose_name="Agent UUID")
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    active = models.BooleanField(verbose_name="Active FLAG",default=False)
    online = models.BooleanField(verbose_name="Online FLAG",default=False)
    def __str__(self):
        return f"SL Agent {self.uuid} -is in parcel-> {self.parcel.uuid}: Last Seen: {self.last_seen}"

@admin.register(SLParcelAgent)
class SLParcelAgentAdmin(admin.ModelAdmin):
    pass



from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import uuid

from community.models import Community
from profiles.models import Profile


# Create your models here.
class Script(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    creator = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Script Type',default="application/ply.script.generic",max_length=100)
    name = models.CharField(verbose_name='Script Human-readable name',max_length=1000)
    descr = models.TextField(verbose_name='Script Description')
    function_name = models.CharField(verbose_name='Script Function/Callable Name (no spaces)',max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Script Created/updated')
    body = models.TextField(verbose_name='Script Body')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'function_name'], name='unique_funcname'),
            models.UniqueConstraint(fields=['community', 'name'], name='unique_name')
        ]

    def __str__(self):
        return f"Script {self.name} Callable: {self.function_name} by {self.creator} in community: {self.community.uuid} TYPE: {self.type}"

@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    pass

class ScriptRegistry(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.CASCADE)
    script = models.ForeignKey(Script,verbose_name = "Registry",on_delete=models.CASCADE)
    key = models.CharField(verbose_name='Registry Key',max_length=1000)
    contents_text = models.TextField(verbose_name='Value (Text)')
    contents_json = models.TextField(verbose_name='Value (JSON)',null=True)
    contents_bin = models.BinaryField(verbose_name='Value (BIN)',null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'profile','script','key'], name='unique_keyperpr'),
        ]

    def __str__(self):
        return f"Script Registry for {self.script.name} Callable: {self.function_name} for  {self.profile.profile_id} in community: {self.community.uuid} KEY: {self.key}"


@admin.register(ScriptRegistry)
class ScriptRegistryAdmin(admin.ModelAdmin):
    pass


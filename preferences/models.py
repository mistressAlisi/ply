from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from dynapages.models import Page
import uuid
# Create your models here.

# Timezones:
class Timezone(models.Model):
    tz = models.TextField(verbose_name='TimeZone Code',default='America/New_York')
    timezone = models.TextField(verbose_name='TimeZone Name',default='America/New_York')
    offset = models.TextField(verbose_name='TimeZone Code',default='-05:00')
    active = models.BooleanField(verbose_name="Active",default=True)
    def __str__(self):
            return f"{self.tz}/{self.timezone} ({self.offset})"

@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    pass

# Timezones:
class Theme(models.Model):
    theme_id = models.TextField(verbose_name='Theme ID',default='default')
    name = models.TextField(verbose_name='Theme Name',default='Ply Default Theme')
    active = models.BooleanField(verbose_name="Active",default=True)
    def __str__(self):
            return f"Theme: {self.name} [{self.theme_id}]"


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass

class Preferences(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Preferences Node Updated')
    shortdate = models.TextField(verbose_name='Short Date Time Format for Output',default='%x',max_length=50)
    longdate = models.TextField(verbose_name='Long Date Format for Output',default='%c',max_length=50)
    time = models.TextField(verbose_name='Time Format for Output',default='%I:%M:%S',max_length=50)
    timezone = models.ForeignKey(Timezone,verbose_name='TimeZone Code',on_delete=models.RESTRICT,null=True,blank=True)
    theme = models.ForeignKey(Theme,verbose_name='System Theme',on_delete=models.RESTRICT,null=True,blank=True)
    stream_top = models.BooleanField(verbose_name="Scroll Streams Top-Down",default=False)
    messages_top = models.BooleanField(verbose_name="Scroll Messages Top-Down",default=False)
    def __str__(self):
            return f"Settings/Preferences Node for user: {self.user.username}"

@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    pass

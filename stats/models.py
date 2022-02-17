from django.db import models
from community.models import Community
from profiles.models import Profile
import uuid
from django.contrib import admin
# Create your models here.


# Base Stats definitions:
class BaseStat(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    name = models.TextField(verbose_name='Name')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(verbose_name='Updated',auto_now_add=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    minimum = models.IntegerField(verbose_name='Minimum Value',default=0)
    maximum = models.IntegerField(verbose_name='Maximum Value',default=10)
    starting = models.IntegerField(verbose_name='Starting Value',default=1)
    def __str__(self):
        return f"Base Stat: {self.name}, in community: {self.community.name}: Min: {self.minimum}, Max: {self.maximum}, Starting: {self.starting}"
@admin.register(BaseStat)
class BaseStatAdmin(admin.ModelAdmin):
    pass  

# Apply each Stat, per Profile, per Community - and track it's state:
class ProfileStat(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile  = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.RESTRICT)
    stat = models.ForeignKey(BaseStat,verbose_name="Community",on_delete=models.CASCADE)
    updated = models.DateTimeField(verbose_name='Updated',auto_now_add=True)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    pminimum = models.IntegerField(verbose_name='Minimum Value',default=0)
    pmaximum = models.IntegerField(verbose_name='Maximum Value',default=10)
    value = models.IntegerField(verbose_name='Current Value',default=1)
    def __str__(self):
        return f"Profile Stat: {self.name}, in community: {self.community.name} Applied to Profile {self.profile.name}: Min: {self.pminimum}, Max: {self.pmaximum}, Current Value: {self.value}"
@admin.register(ProfileStat)
class ProfileStatAdmin(admin.ModelAdmin):
    pass  

# Track each stat change using a history table linked to the aforementioned profile/community/stat table defined above:
class ProfileStatHistory(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile  = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.RESTRICT)
    stat = models.ForeignKey(BaseStat,verbose_name="Community",on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Updated',auto_now_add=True)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    pminimum = models.IntegerField(verbose_name='Minimum Value',default=0)
    pmaximum = models.IntegerField(verbose_name='Maximum Value',default=10)
    value = models.IntegerField(verbose_name='Current Value',default=1)
    notes = models.TextField(verbose_name='Name')
    def __str__(self):
        return f"Profile Stat History: {self.name}, in community: {self.community.name} Applied to Profile {self.profile.name}: Min: {self.pminimum}, Max: {self.pmaximum}, Current Value: {self.value}, Date: {self.created}" 
@admin.register(ProfileStatHistory)
class ProfileStatHistoryAdmin(admin.ModelAdmin):
    pass  

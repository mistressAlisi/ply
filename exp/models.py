import uuid
from django.db import models
from django.contrib import admin
from community.models import Community
from profiles.models import Profile
from plyscript.models import Script
from stats.models import ClassType
# Create your models here.
class Level(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    level = models.IntegerField(verbose_name='Level (Numeric Value)',default=1)
    name = models.TextField(verbose_name='Name')
    expr = models.IntegerField(verbose_name='Experience Required',default=0)
    statpoints = models.IntegerField(verbose_name='Stat Points Awarded',default=5)
    script = models.ForeignKey(Script,verbose_name="Run Script on Awarding Level",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(verbose_name='Updated',auto_now_add=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'level'], name='unique_level'),
        ]
    def __str__(self):
        return f"Level: {self.level}, in community: {self.community.name}: Exp Required: {self.expr}, Statpoints granted: {self.statpoints}"
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


class LevelScript(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    classtype = models.ForeignKey(ClassType,verbose_name = "Class Type",on_delete=models.CASCADE)
    level = models.ForeignKey(Level,verbose_name = "Level Reached",on_delete=models.CASCADE)
    script = models.ForeignKey(Script,verbose_name = "Script Callable",on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community','classtype','script', 'level'], name='unique_class_level_script'),
        ]
    def __str__(self):
        return f"Level Script: Call {self.script.function_name}, in community: {self.community.name}: For Class Type: {self.classtype.name}, At Level: {self.level.level}"

@admin.register(LevelScript)
class LevelScriptAdmin(admin.ModelAdmin):
    pass

class ProfileExperience(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.CASCADE)
    classtype = models.ForeignKey(ClassType,verbose_name = "Class Type",on_delete=models.CASCADE)
    level = models.ForeignKey(Level,verbose_name = "Current Level",on_delete=models.CASCADE)
    expr = models.IntegerField(verbose_name='Current Experience',default=0)
    statpoints = models.IntegerField(verbose_name='Stat Points Available',default=0)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community','profile'], name='unique_profile_exp'),
        ]

    def can_level(self):
        try:
            new_level = Level.objects.get(level=self.level.level+1,archived=False,blocked=False,frozen=False)
        except Level.DoesNotExist:
            return False
        if (new_level.expr <= self.expr):
            return True
        else:
            return False

    def next_level(self):
        try:
            new_level = Level.objects.get(level=self.level.level+1,archived=False,blocked=False,frozen=False)
        except Level.DoesNotExist:
            return False
        return new_level.level

    def exp_to_level(self):
        try:
            new_level = Level.objects.get(level=self.level.level+1,archived=False,blocked=False,frozen=False)
        except Level.DoesNotExist:
            return False
        return new_level.expr

    def __str__(self):
        return f"Profile Experience: Profile {self.profile.profile_id}, in community: {self.community.name}: Current Experience: {self.expr}  Class Type: {self.classtype.name}, Current Level: {self.level.level}"

@admin.register(ProfileExperience)
class ProfileExperienceAdmin(admin.ModelAdmin):
    pass

from django.db import models
from communities.community.models import Community
from communities.profiles.models import Profile
from django.contrib import admin
import uuid
# Create your models here.
class DiceEvent(models.Model):
    class Meta:
        db_table ="roleplaying_plydice_dice_event"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    date = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Event Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "Author",on_delete=models.RESTRICT)
    type = models.TextField(verbose_name='Event Type')
    count = models.IntegerField(verbose_name='Dice Count',default=1)
    sides = models.IntegerField(verbose_name='Number of Sides',default=12)
    contents_json = models.JSONField(verbose_name='Verbose Event Data',blank=True,null=True)
    def __str__(self):
        return f"Dice Event: {self.count}D{self.sides} by profile-> {self.profile.uuid} in community: {self.community.uuid} TYPE: {self.type}"

@admin.register(DiceEvent)
class DiceEventAdmin(admin.ModelAdmin):
    pass

class DiceRoll(models.Model):
    class Meta:
        db_table = "roleplaying_plydice_dice_roll"
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    date = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Roll Time')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.RESTRICT)
    type = models.TextField(verbose_name='Roll Type')
    count = models.IntegerField(verbose_name='Dice Count',default=1)
    sides = models.IntegerField(verbose_name='Number of Sides',default=12)
    result = models.IntegerField(verbose_name='Results ',default=0)
    threshold = models.IntegerField(verbose_name='Threshold ',default=6)
    contents_json = models.JSONField(verbose_name='Verbose Roll Data',blank=True,null=True)
    def __str__(self):
        return f"Dice Roll: {self.count}D{self.sides} (Threshold: {self.threshold}) -for profile-> {self.profile.uuid} in community: {self.community.uuid} TYPE: {self.type}"

@admin.register(DiceRoll)
class DiceRollAdmin(admin.ModelAdmin):
    pass

class DiceEventRoll(models.Model):
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    event = models.ForeignKey(DiceEvent,verbose_name="Event",on_delete=models.CASCADE)
    roll = models.ForeignKey(DiceRoll,verbose_name="Roll",on_delete=models.CASCADE)
    class Meta:
        db_table = "roleplaying_plydice_dice_event_roll"
        constraints = [
            models.UniqueConstraint(fields=['event', 'roll'], name='unique_roll')
        ]

@admin.register(DiceEventRoll)
class DiceEventRollAdmin(admin.ModelAdmin):
    pass

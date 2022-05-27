from django.db import models
from community.models import Community
from profiles.models import Profile
from django.contrib import admin
import uuid
# Create your models here.
class DiceRoll(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    date = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Roll Time')
    profile = models.ForeignKey(Profile,verbose_name = "Author",on_delete=models.RESTRICT)
    type = models.TextField(verbose_name='Roll Type')
    count = models.IntegerField(verbose_name='Dice Count',default=1)
    sides = models.IntegerField(verbose_name='Number of Sides',default=12)
    result = models.IntegerField(verbose_name='Results ',default=0)
    threshold = models.IntegerField(verbose_name='Threshold ',default=6)
    contents_json = models.JSONField(verbose_name='Verbose Roll Data',blank=True,null=True)
    def __str__(self):
        return f"Stream Message: {self.uuid} -in stream-> {self.stream.uuid} in community: {self.stream.community.uuid} TYPE: {self.type}"

@admin.register(DiceRoll)
class DiceRollAdmin(admin.ModelAdmin):
    pass

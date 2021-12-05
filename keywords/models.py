from django.db import models
from django.contrib import admin
# Create your models here.


class Keyword(models.Model):
    keyword = models.TextField(max_length=200,verbose_name='Keyword')
    hash =  models.TextField(max_length=200,verbose_name='Hash')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Item Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='tem Updated')
    items = models.IntegerField(verbose_name='Item Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    likes = models.IntegerField(verbose_name='Likes Count',default=0)
    dislikes = models.IntegerField(verbose_name='DisLikes Count',default=0)
    shares = models.IntegerField(verbose_name='Shares Count',default=0)
    comments = models.IntegerField(verbose_name='Comment Count',default=0)
    active = models.BooleanField(verbose_name="Active FLAG",default=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"{self.keyword} ({self.hash})"
    
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass   

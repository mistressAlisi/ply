from django.db import models
from django.contrib import admin
# Create your models here.
class Discipline(models.Model):
    class Meta:
        db_table ="content_manager_categories_discipline"
    name = models.TextField(max_length=200,verbose_name='Discipline Name')
    hash =  models.TextField(max_length=200,verbose_name='Hash')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Updated')
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
        return f"Discipline: {self.name} (%{self.hash})"

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass


class Category(models.Model):
    name = models.TextField(max_length=200,verbose_name='Category Name')
    hash =  models.TextField(max_length=200,verbose_name='Hash')
    discipline = models.ForeignKey(Discipline,verbose_name='Discipline Name',on_delete=models.CASCADE)
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
    class Meta:
        db_table ="content_manager_categories_category"
        constraints = [
            models.UniqueConstraint(fields=['hash', 'discipline'], name='unique_hashdis')
        ]
    def __str__(self):
        return f"{self.discipline.name}:{self.name}"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import uuid
# Create your models here.


class Templates(models.Model):
    template_id = models.TextField(max_length=200,verbose_name='Template ID')
    label = models.TextField(max_length=200,verbose_name='Template Label')
    filename = models.TextField(max_length=200,verbose_name='Template Filename')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Template Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Template Updated')
    creator = models.TextField(max_length=200,verbose_name = "Creator",default='system')
    description = models.TextField(max_length=2000,verbose_name = "Description",default='a template page')
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    page_template = models.BooleanField(verbose_name="Template is used for Pages",default=True)
    widget_template = models.BooleanField(verbose_name="Template is used for Widgets",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"Dynapage Template [{self.template_id}] Label: '{self.label}' filename: '{self.filename}'"

@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    pass    
    

class Widget(models.Model):
    widget_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    label = models.TextField(max_length=200,verbose_name='Widget Label')
    descr = models.TextField(max_length=200,verbose_name='Widget Description')
    helptext = models.TextField(max_length=200,verbose_name='Widget Helptext')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Widget Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Widget Updated')
    version = models.IntegerField(verbose_name='Widget Vers')
    plugin = models.TextField(verbose_name="Widget Plugin",default='',null=True)
    widget_data = models.JSONField(verbose_name="Widget plugin-specific data",blank=True,null=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    template = models.ForeignKey(Templates,verbose_name = "Dynapage Template",on_delete=models.CASCADE)
    banner = models.BooleanField(verbose_name="Includes Banner Mode",default=False)
    mainbody = models.BooleanField(verbose_name="Includes MainBody Mode",default=True)
    sidecol = models.BooleanField(verbose_name="Includes SideColumn Mode",default=False)
    footer = models.BooleanField(verbose_name="Includes Footer Mode",default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)

    def __str__(self):
        return f"Dynapage Widget: {self.label}"

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    pass    
    
    
    
class Page(models.Model):
    page_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    slug = models.TextField(max_length=200,verbose_name='Page slug')
    label = models.TextField(max_length=200,verbose_name='Page Label')
    template = models.ForeignKey(Templates,verbose_name = "Dynapage Template",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Page Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Page Updated')
    creator = models.ForeignKey(User,verbose_name = "User",on_delete=models.CASCADE)
    def __str__(self):
        return f"Dynapage Page: {self.slug}. Created by {self.creator}"

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass    
 
 
class PageWidget(models.Model):
    pagewidget_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    page = models.ForeignKey(Page,verbose_name = "DynaPage",on_delete=models.CASCADE)
    widget = models.ForeignKey(Widget,verbose_name = "Widget",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Widget Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Widget Updated')
    banner = models.BooleanField(verbose_name="Banner Mode",default=False)
    mainbody = models.BooleanField(verbose_name="MainBody Mode",default=False)
    sidecol = models.BooleanField(verbose_name="SideColumn Mode",default=False)
    footer = models.BooleanField(verbose_name="Footer Mode",default=False)
    pos = models.TextField(max_length=200,verbose_name='Widget Position (Column)',null=True,blank=True)
    order = models.IntegerField(verbose_name='Widget Order',default=0)
    thumbnail = models.TextField(verbose_name="Widget Thumbnail",default='',null=True,blank=True)
    plugin_data = models.JSONField(verbose_name="Widget plugin-specific data",blank=True,null=True)
    
    def __str__(self):
        return f"Dynapage Page Widget: {self.widget.label} in {self.page.label}, Order: {self.order} for [B:{self.banner}|M:{self.mainbody}|S:{self.sidecol}|F:{self.footer}]"

@admin.register(PageWidget)
class PageWidgetAdmin(admin.ModelAdmin):
    pass    
    

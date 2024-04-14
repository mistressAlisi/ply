from django.db import models

from communities.community.models import Community


# Create your models here.

class GalleryPhotoSettings(models.Model):
    class Meta:
        db_table =  "media_gallery_photo_settings"
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True,blank=True,unique=True)
    gallery_max_filesize = models.IntegerField(verbose_name="Maximum File Size in MB",default=25,help_text="The absolute maximum file size allowed in the Gallery in megabytes. All modules are limited by this parameter.")
    enable_exif = models.BooleanField(verbose_name="Enable EXIF Parsing",default=True,help_text="Enable EXIF Parsing Features")
    def __str__(self):
        return f"Gallery Photo Settings for Community: {self.community}"

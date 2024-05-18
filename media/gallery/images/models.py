from django.db import models

from communities.community.models import Community



# Create your models here.
class GalleryImagesFileTypes(models.Model):
    class Meta:
        db_table = "media_gallery_images_filetypes"
    ext = models.CharField(verbose_name="Filename Extension",unique=True)
    mime = models.CharField(verbose_name="File Mimetype")
    name = models.CharField(verbose_name="File Type Name")
    active = models.BooleanField(verbose_name="File Type Active",default=True)
    def __str__(self):
     return f"{self.name} - ext(s): {self.ext} ({self.mime})"


class GalleryImagesSettings(models.Model):
    class Meta:
        db_table =  "media_gallery_images_settings"
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True,blank=True,unique=True)
    max_filesize = models.IntegerField(verbose_name="Maximum File Size in MB",default=25,help_text="The absolute maximum file size allowed in the Gallery in megabytes. All modules are limited by this parameter.")
    enable_exif = models.BooleanField(verbose_name="Enable EXIF Parsing",default=True,help_text="Enable EXIF Parsing Features")
    enable_icc = models.BooleanField(verbose_name="Enable ICC Parsing",default=True,help_text="Enable ICC Colour Profile Parsing Features")
    min_dpi = models.IntegerField(verbose_name="Minimum Recommended DPI",default=150,help_text="Images with lower DPI values will generate a warning, they can still be uploaded.")
    rescaler_enabled = models.BooleanField(verbose_name="Rescale to target device screens",default=True,help_text="When enabled, the gallery will generate device-sized images for all major device resolutions, reducing bandwidth and data usage")
    rescaler_factor = models.DecimalField(verbose_name="Rescaler Factor",help_text="Rescaler Factor to use in scaling down images (default is -0.10 or -10%: i.e. decrements of 10% from the max size)",max_digits=4,decimal_places=2,default=0.1)
    rescaler_target_format = models.OneToOneField(GalleryImagesFileTypes,verbose_name="Rescaler output File Format",help_text="When selected, Rescaler will use this format for output. Otherwise, it will use JPEG",null=True,on_delete=models.RESTRICT,related_name="+")
    rescaler_fallback_jpeg = models.BooleanField(verbose_name="Enable JPEG Fallback",default=True,help_text="When other formats are enabled; also generate a JPEG fallback for older browsers.")
    rescaler_target_quality = models.CharField(verbose_name="Rescaler Quality Parameters",help_text="(Advanced) Output File Format Specific File quality parameters - RTFM!!!!",null=True,blank=True)
    downloads_enabled = models.BooleanField(verbose_name="Enable Downloading Files",default=False,help_text="Allow users to enable downloading of their media files from their galleries.")
    enabled_filetypes = models.ManyToManyField(GalleryImagesFileTypes,verbose_name="Enabled Input Filetypes",help_text="Select which File types are allowed in this Gallery.")
    def __str__(self):
        return f"Gallery Image Settings for Community: {self.community}"


def __galleryGetSettingsObject():
    return GalleryImagesSettings


def __galleryGetFileTypesObject():
    return GalleryImagesFileTypes
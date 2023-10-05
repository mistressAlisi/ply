from django.contrib import admin
from .models import Asset, AssetLog, Area

# Register your models here.

class AssetLogInline(admin.TabularInline):
    model = AssetLog
    extra = 2

class AssetAdmin(admin.ModelAdmin):
    list_display = ['constructAssetTag', 'description', 'type', 'status', 'serial_number', 'storage_location', 'owner']
    list_filter = ('type', 'status', 'storage_location', 'is_convention_owned')
    inlines = [AssetLogInline]

admin.site.register(Asset, AssetAdmin)
admin.site.register(Area)
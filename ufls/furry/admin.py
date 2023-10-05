from django.contrib import admin
from .models import Profile, EmailValidation, RoomMonitorHistory, RoomMonitor
# Register your models here.

class EmailValidationAdmin(admin.ModelAdmin):
    list_display = ['user','used','usedFor','dateCreated']
    list_filter = ('usedFor', 'used')

admin.site.register(EmailValidation, EmailValidationAdmin)
admin.site.register(Profile)
admin.site.register(RoomMonitor)
admin.site.register(RoomMonitorHistory)
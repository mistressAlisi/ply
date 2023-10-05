from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Announcement,
    Department,
    OpenPosition,
    StaffApplication,
    StaffAssignment,
    StaffTask,
    TaskTemplate, LicenseKey,
)

# Register your models here.


def mass_hide(modeladmin, request, queryset):
    for x in queryset:
        x.hidden = True
        x.save()


mass_hide.short_description = "Hide from Positions Page"


def mass_show(modeladmin, request, queryset):
    for x in queryset:
        x.hidden = False
        x.save()


mass_show.short_description = "Show on Positions Page"


class OpenPositionAdmin(admin.ModelAdmin):
    list_display = ["name", "department", "need", "hidden"]
    list_filter = ["hidden", "department"]
    list_editable = ["hidden"]
    actions = [mass_hide, mass_show]

def closeApps(modeladmin, request, queryset):
    for x in queryset:
        x.closeApp = True
        x.save()

class StaffApplicationAdmin(ImportExportModelAdmin):
    def applicant_name(self):
        return f"{self.firstName} {self.lastName}"

    list_display = ["fanName", applicant_name, "openPosition", "closeApp"]
    list_filter = ["closeApp", "openPosition"]
    search_fields = ["lastName", "firstName", "fanName"]
    actions = [closeApps]

class LicenseKeyAdmin(ImportExportModelAdmin):
    list_display = ['key','program','assigned']

admin.site.register(Department)
admin.site.register(OpenPosition, OpenPositionAdmin)
admin.site.register(StaffAssignment)
admin.site.register(StaffApplication, StaffApplicationAdmin)
admin.site.register(TaskTemplate)
admin.site.register(StaffTask)
admin.site.register(Announcement)
admin.site.register(LicenseKey, LicenseKeyAdmin)

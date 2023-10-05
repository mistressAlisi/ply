from django.contrib import admin
from .models import Application, StatusMessage, ReservationKey
from import_export.admin import ImportExportModelAdmin
from ufls.celery import app as Celery
# Register your models here.

def sendLinkAsync(modeladmin, request, queryset):
    lst = []
    for x in queryset:
        lst.append([x.email,x.link()])
        x.sent = True
        x.save()
    Celery.send_task(name='registration.tasks.sendHotelLinksToEmails', kwargs={"lst": lst})

sendLinkAsync.short_description = "2023 - Send e-mails with Link"

def sendHotelTransmit(modeladmin, request, queryset):
    lst = []
    for x in queryset:
        lst.append([x.email,x.link()])
        x.sent = True
        x.save()
    Celery.send_task(name='registration.tasks.sendHotelTransmit', kwargs={"lst": lst})

sendHotelTransmit.short_description = "2022 - Send hotel transmit confirmation"

def sendLinkReminderAsync(modeladmin, request, queryset):
    lst = []
    for x in queryset:
        lst.append([x.email,x.link()])
        x.sent = True
        x.save()
    Celery.send_task(name='registration.tasks.sendHotelLinkRemindersToEmails', kwargs={"lst": lst})

sendLinkReminderAsync.short_description = "2023 - Send REMINDER e-mails with Link"

class ReservationKeyAdmin(ImportExportModelAdmin):
    list_display = ['email', 'group', 'key', 'used', 'sent']
    list_filter = ['group']
    actions = [sendLinkAsync, sendLinkReminderAsync, sendHotelTransmit]

class ApplicationAdmin(ImportExportModelAdmin):
    list_display = ['title', 'author', 'code', 'enabled', 'staff_only', 'show_on_app_list']

admin.site.register(Application, ApplicationAdmin)
admin.site.register(StatusMessage)
admin.site.register(ReservationKey, ReservationKeyAdmin)
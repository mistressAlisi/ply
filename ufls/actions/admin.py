from django.contrib import admin
from .models import Action


class ActionAdmin(admin.ModelAdmin):
    list_filter = ['read', 'completed', 'dateEntered']
    list_display = ['id', 'initiator', 'owner', 'isDelegated', 'subject', 'read', 'completed', 'dateEntered']

# Register your models here.

admin.site.register(Action, ActionAdmin)
from django.urls import path, include
from . import forge_api_views as views

urlpatterns = [
    path("settings/set", views.settings_save, name="Save Gallery Settings"),
    path("settings/set/plugin", views.plugin_settings_save, name="Save Gallery Settings"),
]

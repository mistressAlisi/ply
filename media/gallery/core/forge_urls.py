from django.urls import path, include
from . import forge_views as views

urlpatterns = [
    path("api/", include("media.gallery.core.forge_api_urls")),
    path("setup", views.setup, name="Setup"),
    path("setup/plugin/<str:plugin>",views.plugin_setup,name="Plugin Setup View")
]

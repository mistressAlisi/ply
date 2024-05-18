from django.urls import path, include
from . import forge_views as views

urlpatterns = [
    path("studio", views.dashboard_studio),
]

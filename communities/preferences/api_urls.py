from django.urls import path
from communities.preferences import api_views

urlpatterns = [
    path('save/settings', api_views.save_system_settings),
]


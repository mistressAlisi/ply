from django.urls import path,include
from communities.preferences import dashboard_views

urlpatterns = [
    path('system', dashboard_views.system_settings),
    path('api/',include('communities.preferences.api_urls')),
]

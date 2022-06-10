from django.urls import path,include
from preferences import dashboard_views

urlpatterns = [
    path('system',dashboard_views.system_settings),
    path('api/',include('preferences.api_urls')),
]

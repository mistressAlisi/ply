from django.contrib import admin
from django.urls import path,include
urlpatterns = [
path('', include('core.forge.user_urls')),
path('', include('core.forge.admin_urls')),
path('api/', include('core.forge.api_urls'))
]
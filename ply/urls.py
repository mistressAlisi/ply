"""pixel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .auth_views import login

urlpatterns = [
    path('profiles/',include('profiles.public_urls')),
    path('p/', include('profiles.sharing_urls')),
    path('almanac/',include('almanac.public_urls')),    
    path('almanac/user/',include('almanac.user_urls')),    
    path('dashboard/user/',include('dashboard.user_urls')),
    path('keywords/api/',include('keywords.api_urls')),
    path('forge/', include('forge.user_urls')),
    path('forge/', include('forge.admin_urls')),
    path('forge/api/', include('forge.api_urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('ply.api_urls')),
    path('martor/', include('martor.urls')),
    path('gallery/', include('gallery.public_urls')),
    path('g/', include('gallery.sharing_urls')),
    path('stream/', include('stream.public_urls')),
    path('stream/api/', include('stream.api_urls')),
    path('SLHUD/', include('SLHUD.hud_urls')),
    path('SLHUD/api/', include('SLHUD.api_urls')),
    #path('s/', include('gallery.sharing_urls')),
    path('', include('community.public_urls'))
]

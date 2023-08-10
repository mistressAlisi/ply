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
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('profiles/',include('communities.profiles.public_urls')),
    path('p/', include('communities.profiles.sharing_urls')),
    path('s/k/', include('content_manager.keywords.sharing_urls')),
    path('dynapages/api/',include('core.dynapages.api_urls')),
    path('almanac/',include('content_manager.almanac.public_urls')),
    path('almanac/user/',include('content_manager.almanac.user_urls')),
    path('dashboard/user/',include('dashboard.user_urls')),
    path('keywords/api/',include('content_manager.keywords.api_urls')),
    path('forge/', include('core.forge.user_urls')),
    path('forge/', include('core.forge.admin_urls')),
    path('forge/api/', include('core.forge.api_urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('ply.api_urls')),
    path('martor/', include('martor.urls')),
    # path('core/', include('core.public_urls')),
    # path('g/', include('core.sharing_urls')),
    path('stream/', include('communities.stream.public_urls')),
    path('stream/api/', include('communities.stream.api_urls')),
    path('stats/api/', include('roleplaying.stats.api_urls')),
    path('SLHUD/', include('roleplaying.SLHUD.hud_urls')),
    path('SLHUD/api/', include('roleplaying.SLHUD.api_urls')),
    path('dice/api/',include('roleplaying.plydice.api_urls')),
    path('', include('communities.community.public_urls'))
]

"""ply URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin

from . import settings
from django.urls import path, include
from ply import settings
import ply
from .auth_views import login
from .toolkit.core import get_ply_appinfo


urlpatterns = [
    #path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path("profiles/", include("communities.profiles.public_urls")),
    path("gallery/",include("media.gallery.core.public_urls")),
    path("gallery/api/",include("media.gallery.core.public_api_urls")),
    path("g/",include("media.gallery.core.sharing_urls")),
    path("p/", include("communities.profiles.sharing_urls")),
    path("s/k/", include("content_manager.keywords.sharing_urls")),
    path("dynapages/api/", include("core.dynapages.api_urls")),
    path("almanac/", include("content_manager.almanac.public_urls")),
    path("almanac/user/", include("content_manager.almanac.user_urls")),
    path("dashboard/", include("dashboard.urls")),
    path("keywords/api/", include("content_manager.keywords.api_urls")),
    path("forge/", include("core.forge.urls")),
    path("accounts/", include("core.authentication.ui.urls")),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/api/", include("django.contrib.auth.urls")),
    path("accounts/api/", include("django_registration.backends.activation.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("ply.api_urls")),
    path('app/ufls/return/', include('ufls.backend_connection_urls')),
    path("martor/", include("martor.urls")),
    path("stream/", include("communities.stream.public_urls")),
    path("stream/api/", include("communities.stream.api_urls")),
    path("stats/api/", include("roleplaying.stats.api_urls")),
    path("SLHUD/", include("roleplaying.SLHUD.hud_urls")),
    path("SLHUD/api/", include("roleplaying.SLHUD.api_urls")),
    path("dice/api/", include("roleplaying.plydice.api_urls")),
    path("stripe/", include('djstripe.urls', namespace='djstripe')),
    path("", include("communities.community.public_urls"))
]
# The following is for Dynamic Application URL loading using ply_appinfo.app_endpoints:
if settings.PLY_DYNAMIC_APP_URLS_ENABLED:
    assigned = []
    for app in settings.INSTALLED_APPS:
        app_data = get_ply_appinfo(app)
        if app_data:
            if "app_endpoints" in app_data.PLY_APP_INFO:
                endpoints = app_data.PLY_APP_INFO["app_endpoints"]
                for ep in endpoints:
                    if app_data.PLY_APP_INFO["app_endpoints"][ep]["enable"]:
                        if app_data.PLY_APP_INFO["app_endpoints"][ep]["url_base"] not in assigned:
                            urlpatterns += [path(f'app/{app_data.PLY_APP_INFO["app_endpoints"][ep]["url_base"]}/',include(app_data.PLY_APP_INFO["app_endpoints"][ep]["module"]))]
                            assigned.append(app_data.PLY_APP_INFO["app_endpoints"][ep]["url_base"])
"""
# UFLS URLs:
urlpatterns += [
    # Registrar App paths:
    path('app/api/', include('ufls.registrar.api_urls')),
    path('app/registrar/', include('ufls.registrar.urls')),
    path('app/ufls/return/', include('ufls.backend_connection_urls')),
    path('app/marketplace/', include('ufls.dealers.dealer_front_urls')),
    path('app/marketplace/registration/', include('ufls.dealers.urls')),
    path('app/marketplace/api/', include('ufls.dealers.urls')),
    path('app/marketplace/admin/', include('ufls.dealers.admin_urls')),
    #path('app/training/', include('ufls.training.urls')),
    path('app/schedule/', include('ufls.scheduling.events_front_urls')),
    path('app/schedule/backend/', include('ufls.scheduling.urls')),
]
"""
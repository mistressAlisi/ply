"""ufls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.urls import path, include
from django.core.mail import send_mail
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, status, permissions
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from connections.views import fetchByOTPKey, getScope, getReservation, postReservation
from furry.views import verify, newPassword

from ufls import views as ufls_views
from marketplace import views as marketplace_views

from registration import views as registration_views


from ufls.celery import app as Celery



from rest_framework_simplejwt.tokens import RefreshToken

from ufls.serializers import UserViewSet, StatusMessageViewSet, RoomMonitorViewSet, RoomMonitorHistoryViewSet


# REST ViewSets:
from inventory.viewsets import AssetViewSet, AssetPOSTViewSet, AssetBoxViewSet, AssetGlimpseViewSet, AreaViewSet
from actions.viewsets import ActionViewSet
from event.viewsets import LocationViewSet,HotTableViewSet,InvoiceViewSet
from marketplace.viewsets import TableSizeViewSet,ArtistAlleyViewSet,DealerAssistantViewSet,TableDefinitionViewSet,TableAssignmentViewSet,DealerViewSet
from registration.viewsets import PrintJobViewSet, RegistrantDataViewSet, EventViewSet, RegistrantDataGlimpseViewSet, \
    BadgeViewSet

#STAFF REST ViewSets:
from staff import viewsets as staff_viewsets
from staff_onboarding import viewsets as staff_onboard_viewsets

# REST router:
router = routers.SimpleRouter()
router.register(r'api/v1/users', UserViewSet)
router.register(r'api/v1/staff', staff_viewsets.StaffAssignmentPublicViewSet)
router.register(r'api/v1/messages', StatusMessageViewSet)
router.register(r'api/v1/printjobs', PrintJobViewSet)
router.register(r'api/v1/rooms', RoomMonitorViewSet)
router.register(r'api/v1/room-history', RoomMonitorHistoryViewSet)
router.register(r'api/v1/registrants', RegistrantDataViewSet)
router.register(r'api/v1/badges', BadgeViewSet)
router.register(r'api/v1/registrants-glimpse', RegistrantDataGlimpseViewSet)
router.register(r'api/v1/events', EventViewSet)
router.register(r'api/v1/inventory/assets', AssetViewSet)
router.register(r'api/v1/inventory/assets-post', AssetPOSTViewSet)
router.register(r'api/v1/inventory/boxes', AssetBoxViewSet)
router.register(r'api/v1/inventory/asset-glimpse', AssetGlimpseViewSet)
router.register(r'api/v1/inventory/areas', AreaViewSet)
router.register(r'api/v1/actions', ActionViewSet)
router.register(r'api/v1/event/hottable', HotTableViewSet)
router.register(r'api/v1/event/invoice', InvoiceViewSet)
router.register(r'api/v1/mkt/table/size', TableSizeViewSet)
router.register(r'api/v1/mkt/table/define', TableDefinitionViewSet)
router.register(r'api/v1/mkt/table/assign', TableAssignmentViewSet)
router.register(r'api/v1/mkt/alley', ArtistAlleyViewSet)
router.register(r'api/v1/mkt/dealer/assistant', DealerAssistantViewSet)
router.register(r'api/v1/mkt/dealer/dealer', DealerViewSet)

# REST STAFF ROUTER:

staff_router = routers.SimpleRouter()
staff_router.register(r'api/v1/staff/department', staff_viewsets.DepartmentViewSet)
staff_router.register(r'api/v1/staff/open', staff_viewsets.OpenPositionViewSet)
staff_router.register(r'api/v1/staff/licensekey', staff_viewsets.LicenseKeyViewSet)
staff_router.register(r'api/v1/staff/assignment', staff_viewsets.StaffAssignmentViewSet)
staff_router.register(r'api/v1/staff/application', staff_viewsets.StaffApplicationViewSet)
staff_router.register(r'api/v1/staff/policies', staff_viewsets.PolicyViewSet)
staff_router.register(r'api/v1/staff/tasktemplate', staff_viewsets.TaskTemplateViewSet)
staff_router.register(r'api/v1/staff/task', staff_viewsets.StaffTaskViewSet)
staff_router.register(r'api/v1/staff/announcement', staff_viewsets.AnnouncementViewSet)
staff_router.register(r'api/v1/staff/onboarding', staff_onboard_viewsets.StaffOnboardRecordViewSet,basename="onboard_record")

# FINAL URL Pattern Router:
urlpatterns = [
    path('', ufls_views.index),

    path('connect/', include('foauth.urls')),

    path('admin/', admin.site.urls),
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('django_auth_oidc.urls')),
    path('api/v1/mkt/functions/', include('marketplace.urls')),
    path('api/v1/app/validate-app-code/<str:code>/', ufls_views.validateAppCode),
    path('api/v1/app/get/current-event/', ufls_views.getCurrentEvent),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('account/', include('furry.urls')),
    path('token/', views.obtain_auth_token),
    path('verify/<str:username>/<str:key>/', verify),
    path('newPassword/<str:username>/<str:key>/', newPassword),
    # STAFF Paths:
    path('staff/main', include('staff_frontend.urls')),
    path('staff/onboarding', include('staff_onboarding.urls')),
    # API paths:
    path('api/signup/', ufls_views.create_auth),
    path('api/forgot/', ufls_views.forgotPassword),
    path('api/v1/twilio/', ufls_views.do_twilio),
    path('api/print-queues/', ufls_views.getPrintQueues),
    path('api/v1/functions/account-check/<str:email>/', ufls_views.accountExists),
    path('api/v1/functions/fetchPrinters/<str:type>/', ufls_views.getPrinterQueues),
    path('api/v1/functions/printLabel/<str:pk>/', ufls_views.printAssetLabel),
    path('api/v1/functions/syncRegfox/', registration_views.issueRegfoxSync),
    path('api/v1/badge/print-registrant/<str:id>/', registration_views.printBadge),
    path('api/v1/badge/print-registrant/<str:id>/<str:from_queue>/', registration_views.printBadge),
    path('api/v1/badge/print-back/', registration_views.printBadgeBack),
    path('api/v1/badge/print-lunch/', registration_views.printLunchPass),
    path('api/badge/print-registrant/<str:id>/', registration_views.printBadge),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/authenticate/', ufls_views.get_tokens_for_user, name='token_authenticate'),
    path('api/token/login/', ufls_views.authenticate_get_jwt, name='token_sign_in'),
    # APP Paths:
    path('app/reservations/get/<str:email>/<str:key>/', getReservation),
    path('app/reservations/set/<str:email>/<str:key>/', postReservation),
    path('app/label/print/<str:id>/', registration_views.renderLabel),
    path('app/label/print/<str:id>/pdf/', registration_views.labelerpdf),
    path('app/badge/toHtml/<str:id>/', registration_views.displayBadgeHtml),
    path('app/badge/toPdf/<str:id>/', registration_views.badgeToPdf),
    path('app/badge-back/toHtml/', registration_views.badgeBackToHtml),
    path('app/badge-back/toPdf/', registration_views.badgeBackToPdf),
    path('app/badge-lunch/toHtml/', registration_views.lunchPassToHtml),
    path('app/badge-lunch/toPdf/', registration_views.lunchPassToPdf),
    path('app/export/badges/', registration_views.exportBadges),
    path('app/export/registrants/', registration_views.exportRegistrants),
    path('app/webhooks/regfox/', registration_views.handleRegfoxWebhook),
    path('app/test/receipt-printer/', registration_views.testReceiptPrinter),
    path('app/emergency/upload-custom-artwork/<str:id>/', registration_views.uploadCustomArtwork),
    path('app/system/marketplace/get/dealer/', marketplace_views.getDealerApp), #todo: thing
    path('app/system/marketplace/submit/dealer/', marketplace_views.submitDealersApp), #todo: thing
    path('app/redirect/<str:key>/', getScope, name='launch_scoping'),
    path('app/redirect/<str:key>/<str:rapid>/', getScope, name='launch_scoping_r'),
    path('app/redirect/<str:key>/otp/<str:otp>/', fetchByOTPKey),
    path('app/whoami/', ufls_views.whoami),
    path("app/connect/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("app/auth/", include('django.contrib.auth.urls')),
    # Registrar App paths:
    path('app/registrar/',include('registrar.urls')),

]


# Global API REST Router:
urlpatterns += router.urls
# STAFF API REST Router:
urlpatterns += staff_router.urls

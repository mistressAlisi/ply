from django.contrib import admin
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.urls import path, include
from django.core.mail import send_mail
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, status, permissions
from rest_framework.authtoken import views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from furry.models import EmailValidation, Profile, RoomMonitor, RoomMonitorHistory
from furry import views as furry_views
from connections.models import StatusMessage
from connections.views import getScope, fetchByOTPKey, getReservation, postReservation
from registration import views as registration_views
from registration.models import Event
from registration.viewsets import PrintJobViewSet, RegistrantDataViewSet, EventViewSet, RegistrantDataGlimpseViewSet
from inventory.viewsets import AreaViewSet, AssetGlimpseViewSet, AssetViewSet, AssetBoxViewSet, AssetPOSTViewSet
from inventory.models import Asset
from utility.models import Printer
from utility.serializers import PrinterSerializer
from registration.serializers import EventSerializer
from ufls.celery import app as Celery
from twilio.rest import Client
import json, os
from decouple import config
from ufls import serializers as ufls_serialisers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def getPrintQueues(request):

    queues = {
        ####After Hours Config
#                "mainqueue": ["DC6", "DC5"],
        #####Prod Config
        "mainqueue": ["DC3", "DC6", "DC7"],
        "minor15queue": ["DC1"],
        "minor14queue": ["DC1"],
        "daypassqueue": ["DC4", "DC4"],
        "dealersdenqueue": ["DC5"],
        "blackonly": ["DC1", "DC4"]
        #"blackonly": ["DC1", "DC2", "DC4"]
    }

    return JsonResponse(queues, safe=False)



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_auth(request):
    serialized = ufls_serialisers.UserSerializer(data=request.data)
    if serialized.is_valid():

        check = User.objects.filter(email=serialized.data['email'].lower()).first()
        if(check != None):
            return Response("E-mail already registered in UFLS.", status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            serialized.data['email'].lower(),
            serialized.data['email'].lower(),
            serialized.data['password']
        )
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user)
        email = EmailValidation.objects.create(
            user=user,
            usedFor='verification.email.firstCreate'
        )
        #todo: email
        send_mail(
            'Furrydelphia UFLS - Verify your E-mail',
            'Please click the following link to verify your account creation at Furrydelphia. If you did not request this, you can safely ignore this message. https://backend.furrydelphia.org/verify/%s/%s/' % (user.email, email.key),
            'bots@furrydelphia.org',
            [user.email],
            fail_silently=False
        )

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def do_twilio(request):
    d = request.data

    n = d

    # {"message
    #  "to

    to = {
        "yuuki": "+12676290819",
        "drayne": "+16105638387",
        "fray": "+12675350675",
        "hype": "+16102487909"
    }

    account = config("UFLS_TWILIO_ACCOUNT", default="")
    token = config("UFLS_TWILIO_TOKEN", default="")
    from_number = config("UFLS_TWILIO_NUMBER", default="")

    client = Client(account, token)

    if(n['to'] != "everyone"):

        body = """
            ⚠️👸⚠️👸⚠️👸⚠️👸⚠️👸️⚠️\n
            %s\n
            ⚠️👸⚠️👸⚠️👸⚠️👸⚠️👸️⚠️

        """ % (n['message'])

        message = client.messages.create(to=to[n['to']], from_=from_number, body=body)
        if(n['to'] == 'hype'):
            message = client.messages.create(to='+17176396809', from_=from_number, body=body)
    else:
        body = """
            ⛔️👸⛔️👸⛔️👸⛔️👸⛔👸️⛔\n
            %s\n
            ⛔️👸⛔️👸⛔️👸⛔️👸⛔👸️⛔

        """ % (n['message'])

        message = client.messages.create(to=to['yuuki'], from_=from_number, body=body)
        message = client.messages.create(to=to['hype'], from_=from_number, body=body)
        message = client.messages.create(to=to['drayne'], from_=from_number, body=body)
        message = client.messages.create(to=to['fray'], from_=from_number, body=body)

    return Response({"status": "OK"}, status=status.HTTP_201_CREATED)

#        return Response({"status": "NOT OK"}, status=status.HTTP_400_BAD_REQUEST)


def printAssetLabel(request, pk):
    c = get_object_or_404(Asset, tag=pk)
    Celery.send_task(name='brotherlabel.printasset', kwargs={"id": c.tag})
    return JsonResponse({"sent": True}, safe=False)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def forgotPassword(request):
    serialized = ufls_serialisers.UserSerializer(data=request.data)
    if serialized.is_valid():
        user = User.objects.filter(email=serialized.data['email'].lower()).first()
        if (user == None):
            return Response("E-mail not registered in UFLS.", status=status.HTTP_404_NOT_FOUND)
        if(user.is_active == False):
            return Response({"error": "Your account is not activated. Please check your e-mail or contact software@furrydelphia.org."}, status=status.HTTP_412_PRECONDITION_FAILED)
        email = EmailValidation.objects.create(
            user=user,
            usedFor = 'verification.account.resetPassword'
        )
        # todo: email
        send_mail(
            'Furrydelphia UFLS - Password Reset Request',
            'Someone (hopefully you) has requested a Password Reset for your Furrydelphia UFLS account. If you did not request this, you can safely ignore this message. https://backend.furrydelphia.org/newPassword/%s/%s/' % (
            user.email, email.key),
            'bots@furrydelphia.org',
            [user.email],
            fail_silently=False
        )
        return Response(serialized.data, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def whoami(request):
    return JsonResponse({"username": request.user.username, "isStaff": request.user.is_staff, "pk": request.user.pk})


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_tokens_for_user(request):
    refresh = RefreshToken.for_user(request.user)

    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': request.user.username,
        'isStaff': request.user.is_staff
    }, safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def authenticate_get_jwt(request):

    creds = json.loads(request.body)

    login_valid = User.objects.filter(username=creds['username'].lower()).first()

    password_valid = check_password(creds['password'], login_valid.password)
    if(login_valid != None and password_valid):
        login(request, login_valid)

        refresh = RefreshToken.for_user(request.user)

        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': request.user.username,
            'isStaff': request.user.is_staff,
            'pk': request.user.pk
        }, safe=False)
    return JsonResponse({'errors': ['Username or password is invalid']}, status=401)


def index(request):
    return redirect("https://app.furrydelphia.org/auth/login")

@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def accountExists(request, email):
    user = get_user_model().objects.filter(username=email.lower()).first()
    if(user != None):
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

def getPrinterQueues(request, type, queue=None):
    p = Printer.objects.filter(type=type)
    l = {}
    if(type == 'L'):
        l = {
            "l-it": PrinterSerializer(p.filter(queues__contains='l-it'), many=True).data
        }
    if(type == 'R'):
        l = {
            "r-backreg": PrinterSerializer(p.filter(queues__contains='r-backreg'), many=True).data,
            "r-frontreg": PrinterSerializer(p.filter(queues__contains='r-frontreg'), many=True).data,
            "r-frontreg1": PrinterSerializer(p.filter(queues__contains='r-frontreg1'), many=True).data,
            "r-frontreg2": PrinterSerializer(p.filter(queues__contains='r-frontreg2'), many=True).data,
            "r-frontreg3": PrinterSerializer(p.filter(queues__contains='r-frontreg3'), many=True).data,
            "r-frontreg4": PrinterSerializer(p.filter(queues__contains='r-frontreg4'), many=True).data,
            "r-frontreg5":  PrinterSerializer(p.filter(queues__contains='r-frontreg5'), many=True).data,
        }
    if(type == 'B'):
        l = {
            "mainqueue": PrinterSerializer(p.filter(queues__contains='mainqueue'), many=True).data,
            "minor15queue": PrinterSerializer(p.filter(queues__contains='minor15queue'), many=True).data,
            "minor14queue": PrinterSerializer(p.filter(queues__contains='minor14queue'), many=True).data,
            "daypassqueue": PrinterSerializer(p.filter(queues__contains='daypassqueue'), many=True).data,
            "dealersdenqueue": PrinterSerializer(p.filter(queues__contains='dealersdenqueue'), many=True).data,
            "blackonly": PrinterSerializer(p.filter(queues__contains='blackonly'), many=True).data,
        }
    return JsonResponse(l)

cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="2")

def validateAppCode(request, code):
    event = Event.objects.filter(pk=cur_event_pk).first()
    if(event == None):
        return JsonResponse({"stauts": "ERR"}, safe=False)
    if(event.eventAppCode == code):
        return JsonResponse({"status": "OK"}, safe=False)
    return JsonResponse({"status": "BAD"}, safe=False)

def getCurrentEvent(request):
    event = Event.objects.filter(pk=cur_event_pk).first()
    if(event == None):
        return JsonResponse({"stauts": "ERR"}, safe=False)
    if(event.active):
        return JsonResponse(EventSerializer(instance=event).data, safe=False)
    return JsonResponse({"status": "BAD"}, safe=False)
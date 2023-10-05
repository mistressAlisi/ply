from rest_framework.filters import SearchFilter

from .serializers import PrintJobSerializer, RegistrantDataSerializer, EventSerializer, RegistrantDataGlimpseSerializer, \
    BadgeSerializer
from .models import PrintJob, RegistrantData, Event, Badge
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from decouple import config
import os

cur_event_pk = config("UFLS_CURRENT_EVENT_PK", default="")

class PrintJobViewSet(viewsets.ModelViewSet):
    queryset = PrintJob.objects.filter(resolved=False).order_by('timeCreated')
    serializer_class = PrintJobSerializer
    permission_classes = [IsAdminUser]

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['number', 'registrant__conFirstName', 'registrant__conLastName', 'registrant__conBadgeName']
    filterset_fields = ['event', 'number']

class RegistrantDataViewSet(viewsets.ModelViewSet):
    queryset = RegistrantData.objects.all()
    serializer_class = RegistrantDataSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'checkedIn', 'conRegLevel', 'hasMealPlan', 'isForwarding', 'status', 'isCustomPicture']

    def retrieve(self, request, pk=None):
        queryset = RegistrantData.objects.all()
        user = get_object_or_404(queryset, displayId=pk)
        serializer = RegistrantDataSerializer(user)
        return Response(serializer.data)

class RegistrantDataGlimpseViewSet(viewsets.ModelViewSet):
    queryset = RegistrantData.objects.all()
    serializer_class = RegistrantDataGlimpseSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'checkedIn', 'accessibility', 'conRegLevel', 'conFirstName', 'conLastName', 'conCreepFlag', 'conCheckedIn', 'hasMealPlan', 'isForwarding','status','conIsDealerAssistant','conIsDealer','conIsStaff']

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','active']

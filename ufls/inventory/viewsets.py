from .serializers import AreaSerializer, AssetGlimpseSerializer, AssetSerializer, AssetPOSTSerializer
from .models import Area, Asset
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

class AssetViewSet(viewsets.ModelViewSet):
    #queryset = Asset.objects.filter(~Q(status="info"))
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'company', 'is_convention_owned', 'status']

class AssetPOSTViewSet(viewsets.ModelViewSet):
    #queryset = Asset.objects.filter(~Q(status="info"))
    queryset = Asset.objects.all()
    serializer_class = AssetPOSTSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'company', 'is_convention_owned', 'status']

class AssetBoxViewSet(viewsets.ModelViewSet):
    #queryset = Asset.objects.filter(~Q(status="info"))
    queryset = Asset.objects.filter(type='BX')
    serializer_class = AssetSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'company', 'is_convention_owned', 'status']


class AssetGlimpseViewSet(viewsets.ModelViewSet):
    #queryset = Asset.objects.filter(~Q(status="info"))
    queryset = Asset.objects.all()
    serializer_class = AssetGlimpseSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'company', 'is_convention_owned', 'status']

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAdminUser]
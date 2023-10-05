from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from event.models import Location,HotTable,Invoice as EventInvoice




class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]






class HotTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HotTable
        fields = '__all__'

class HotTableViewSet(viewsets.ModelViewSet):
    queryset = HotTable.objects.all()
    serializer_class = HotTableSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]






class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventInvoice
        fields = '__all__'

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = EventInvoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

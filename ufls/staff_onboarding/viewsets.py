from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from staff_onboarding.models import StaffOnboardRecord

class StaffOnboardRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffOnboardRecord
        fields = '__all__'

class StaffOnboardRecordViewSet(viewsets.ModelViewSet):
    queryset = StaffOnboardRecord.objects.all()
    serializer_class = StaffOnboardRecordSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]




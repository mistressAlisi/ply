from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

import ufls.viewsets
from staff.models import Department, OpenPosition, LicenseKey, StaffAssignment, StaffApplication, TaskTemplate, \
    StaffTask, Announcement, Policy
from ufls.permissions import IsAdminOrReadOnly


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]






class OpenPositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenPosition
        fields = '__all__'

class OpenPositionViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = OpenPosition.objects.all()
    serializer_class = OpenPositionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hidden']





class LicenseKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LicenseKey
        fields = '__all__'

class LicenseKeyViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = LicenseKey.objects.all()
    serializer_class = LicenseKeySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]



class StaffAssignmentPublicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffAssignment
        fields = ['user','department','rank','title','primary_assignment','showDisplayTitle', 'grant_access_to_management_panel', 'permissions_matrix']

class StaffAssignmentPublicViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = StaffAssignment.objects.all()
    serializer_class = StaffAssignmentPublicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class StaffAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffAssignment
        fields = '__all__'

class StaffAssignmentViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = StaffAssignment.objects.all()
    serializer_class = StaffAssignmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]






class StaffApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffApplication
        fields = '__all__'

class StaffApplicationViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = StaffApplication.objects.all()
    serializer_class = StaffApplicationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]






class TaskTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = '__all__'

class TaskTemplateViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = TaskTemplate.objects.all()
    serializer_class = TaskTemplateSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]






class StaffTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffTask
        fields = '__all__'

class StaffTaskViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = StaffTask.objects.all()
    serializer_class = StaffTaskSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]






class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class AnnouncementViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class PolicyViewSet(ufls.viewsets.UflsModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
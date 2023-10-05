from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers, viewsets

from connections.models import StatusMessage
from furry.models import EmailValidation, Profile, RoomMonitor, RoomMonitorHistory



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StatusMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusMessage
        fields = '__all__'

class RoomMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMonitor
        fields = '__all__'

class RoomMonitorHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMonitorHistory
        fields = '__all__'

class RoomMonitorViewSet(viewsets.ModelViewSet):
    queryset = RoomMonitor.objects.all()
    serializer_class = RoomMonitorSerializer

class RoomMonitorHistoryViewSet(viewsets.ModelViewSet):
    queryset = RoomMonitorHistory.objects.all()
    serializer_class = RoomMonitorHistorySerializer

class StatusMessageViewSet(viewsets.ModelViewSet):
    queryset = StatusMessage.objects.filter(dateExpires__gte=timezone.now().date())
    serializer_class = StatusMessageSerializer



from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from marketplace.models import TableSize,ArtistAlley,DealerAssistant,TableDefinition,TableAssignment,Dealer
from registration.models import Event
from ufls.viewsets import UflsModelViewSet


class TableSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSize
        fields = '__all__'

class TableSizeViewSet(viewsets.ModelViewSet):
    queryset = TableSize.objects.all()
    serializer_class = TableSizeSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]




class ArtistAlleySerializer(serializers.ModelSerializer):
    AVAIL = (
        ("fri","Friday"),
        ("sat","Saturday"),
        ("sun","Sunday"),
    )
    availability = serializers.MultipleChoiceField(choices=AVAIL)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = ArtistAlley
        fields = '__all__'

class ArtistAlleyViewSet(UflsModelViewSet):
    queryset = ArtistAlley.objects.all()
    serializer_class = ArtistAlleySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'event']
    def create(self, request, *args, **kwargs):
        i = super(ArtistAlleyViewSet, self).create(request, *args, **kwargs)
        accepted = """
        	Hello,<br><br>
        	Someone (hopefully you) has applied to be in the Artists Alley for Furrydelphia 2023<br>
        	This e-mail is to verify that we have recieved your application. Best of Luck!<br>
        Best Wishes,<br>
        Furrydelphia Marketplace Team<br>
        Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org"""

        send_mail("No Action Required - Artists Alley - Application Recieved", "HTML Message Content",
                      'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [i.data['email']],
                      html_message=accepted)
        return i




class DealerAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerAssistant
        fields = '__all__'

class DealerAssistantViewSet(viewsets.ModelViewSet):
    queryset = DealerAssistant.objects.all()
    serializer_class = DealerAssistantSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]






class TableDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableDefinition
        fields = '__all__'

class TableDefinitionViewSet(viewsets.ModelViewSet):
    queryset = TableDefinition.objects.all()
    serializer_class = TableDefinitionSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]






class TableAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableAssignment
        fields = '__all__'

class TableAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TableAssignment.objects.all()
    serializer_class = TableAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]






class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'

    # todo: update, delete, create, and patch needs to be secured.

    def create(self, validated_data):
        instance = super(DealerSerializer, self).create(validated_data)
        from .admin import send_confirmation_recieved
        try:
            send_confirmation_recieved(None, None, [instance])
        except:
            pass
        return instance

class DealerViewSet(UflsModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'event', 'status']



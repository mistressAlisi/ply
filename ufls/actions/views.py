import json

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Action
from .serializers import ActionSerializer

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView


class PatchApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def patch(self, request, notification_id):
        action = Action.objects.get(pk=notification_id, owner=request.user)
        if(request.data['read'] or request.data['completed']):
            serializer = ActionSerializer(action, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=HTTP_200_OK)
        return Response(HTTP_400_BAD_REQUEST)
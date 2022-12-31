from django.urls import path,include
from stream import api_views

urlpatterns = [
    path('create',api_views.create_stream)
]

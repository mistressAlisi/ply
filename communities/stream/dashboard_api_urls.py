from django.urls import path
from communities.stream import api_views

urlpatterns = [
    path('create', api_views.create_stream)
]

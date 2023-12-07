from django.urls import path
from communities.community import forge_views

urlpatterns = [
    path('staff',forge_views.community_staff)
]

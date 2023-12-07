from django.urls import path
from communities.community import forge_api_views

urlpatterns = [
    path('staff/create',forge_api_views.create_community_staff),
    path('staff/delete/<uuid:staff>', forge_api_views.delete_community_staff)
]
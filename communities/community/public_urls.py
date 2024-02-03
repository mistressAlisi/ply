from django.urls import path
from communities.community import public_views

urlpatterns = [
    path('', public_views.community_home)
    
]

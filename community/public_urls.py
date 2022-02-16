from django.urls import path,include
from community import public_views
import ply
urlpatterns = [
    path('',public_views.community_home)
    
]

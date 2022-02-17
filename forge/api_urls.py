from django.urls import path,include
from forge import api_views
import ply
urlpatterns = [
    path('upload/profile/picture/',api_views.upload_profile_picture)
    
]

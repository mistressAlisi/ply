from django.urls import path,include
from forge import api_views
import ply
urlpatterns = [
    path('upload/profile/picture/',api_views.upload_profile_picture),
    path('profile/update/',api_views.update_character_profile),    
    path('profile/finish/',api_views.finish_character_profile)    
]

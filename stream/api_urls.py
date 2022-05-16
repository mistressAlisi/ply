from django.urls import path,include
from stream import api_views
import ply
urlpatterns = [
    path('set/profile/settings',api_views.set_profile_settings)
    #path('profile/update/',api_views.update_character_profile),    
    #path('profile/finish/',api_views.finish_character_profile),
    #path('profile/finish_edit/',api_views.finish_edit_profile),
    #path('upload/community/picture/',api_views.upload_community_picture),
    #path('community/cover/update/',api_views.update_community_profile),    
    #path('community/cover/finish/',api_views.finish_community_profile),

]

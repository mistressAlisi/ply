from django.urls import path
from communities.stream import api_views

urlpatterns = [
    path('set/profile/settings', api_views.set_profile_settings),
    path('publish/@<slug:profile>', api_views.publish_to_profile),
    #path('profile/finish/',api_views.finish_character_profile),
    #path('profile/finish_edit/',api_views.finish_edit_profile),
    #path('upload/community/picture/',api_views.upload_community_picture),
    #path('community/cover/update/',api_views.update_community_profile),    
    #path('community/cover/finish/',api_views.finish_community_profile),

]

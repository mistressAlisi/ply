from django.urls import path
from core.forge import api_views

urlpatterns = [
    path('upload/profile/picture/', api_views.upload_profile_picture),
    path('profile/update/', api_views.update_character_profile),
    path('profile/finish/', api_views.finish_character_profile),
    path('profile/finish_edit/', api_views.finish_edit_profile),
    path('upload/community/picture/', api_views.upload_community_picture),
    path('community/cover/update/', api_views.update_community_profile),
    path('community/cover/finish/', api_views.finish_community_profile),
    path('script/eval/', api_views.script_studio_eval),
    path('script/save/', api_views.script_studio_save),
    path('script/get/<uuid:script>', api_views.script_studio_get)
]

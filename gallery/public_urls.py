from django.urls import path,include
from gallery import public_views
import ply
urlpatterns = [
    path('index',public_views.gallery_home),
    path('@<slug:profile_id>',public_views.profile_gallery),
    path('@<slug:profile_id>/',public_views.profile_gallery),
    path('@<slug:profile_id>/<slug:collection_id>',public_views.profile_gallery_collection),
    path('',public_views.gallery_home)
]

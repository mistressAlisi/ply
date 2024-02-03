from django.urls import path
from communities.stream import public_views

urlpatterns = [
    #path('index',public_views.gallery_home),
    path('@<slug:profile_id>', public_views.profile_steam),
    path('@<slug:profile_id>/', public_views.profile_steam),
    path('_m/<uuid:muuid>', public_views.view_message),
    #path('@<slug:profile_id>/<slug:collection_id>',public_views.profile_gallery_collection),
    path('', public_views.community_stream)
]

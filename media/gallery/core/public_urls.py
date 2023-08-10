from django.urls import path
from media.gallery.core import public_views

urlpatterns = [
    path('index', public_views.gallery_home),
    path('@<slug:profile_id>', public_views.profile_gallery),
    path('@<slug:profile_id>/', public_views.profile_gallery),
    path('@<slug:profile_id>/<slug:collection_id>', public_views.profile_gallery_collection),
    path('', public_views.gallery_home)
]

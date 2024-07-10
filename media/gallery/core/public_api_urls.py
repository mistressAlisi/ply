from django.urls import path, include
from . import api_views as api_views
from . import public_api_views as public_views

urlpatterns = [
    path("get/all_collections/", api_views.gallery_collections_raw),
    path("get/items/<collection>", api_views.gallery_collection_items_raw),
]

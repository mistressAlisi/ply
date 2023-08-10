from django.urls import path
from media.gallery.core import sharing_views

urlpatterns = [
    path('<slug:profile_id>/<uuid:collection_id>/<uuid:item_id>', sharing_views.gallery_item),

]

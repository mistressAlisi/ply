from django.urls import path,include
from gallery import sharing_views
import ply
urlpatterns = [
    path('@<slug:profile_id>/<uuid:collection_id>/<uuid:item_id>',sharing_views.gallery_item),

]

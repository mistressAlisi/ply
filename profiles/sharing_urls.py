from django.urls import path,include
from profiles import sharing_views
import ply
urlpatterns = [
    path('@<slug:profile_id>',sharing_views.profile),

]

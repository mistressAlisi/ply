from django.urls import path,include
from forge import admin_views
urlpatterns = [
    path('edit/community/cover',admin_views.edit_community_cover),
    path('edit/community/cover/preview/',admin_views.edit_community_cover_preview)
]


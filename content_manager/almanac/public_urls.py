from django.urls import path
from content_manager.almanac import public_views

urlpatterns = [
    path('', public_views.almanac_home),
    path('page/<slug:page_id>', public_views.almanac_page)
]

from django.urls import path,include
from almanac import public_views
urlpatterns = [
    path('',public_views.almanac_home),
    path('page/<slug:page_id>',public_views.almanac_page)
]

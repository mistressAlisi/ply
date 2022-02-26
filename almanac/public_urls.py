from django.urls import path,include
from almanac import public_views
urlpatterns = [
    path('',public_views.almanac_home)
]

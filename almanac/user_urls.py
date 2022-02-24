from django.urls import path,include
from almanac import user_views
urlpatterns = [
    path('',user_views.almanac_home)
]

from django.urls import path,include
from profiles import public_views
urlpatterns = [
    path('index',public_views.profile_index),
    path('@<profile_id>',public_views.profile_view),


]


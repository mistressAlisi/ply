from django.urls import path,include
from communities.profiles import public_views
urlpatterns = [
    path('index',public_views.profile_index),
    path('@<slug:profile_id>',public_views.profile_view),


]


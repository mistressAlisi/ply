from django.urls import path,include
from profiles import public_views
urlpatterns = [
    path('<profile_id>',public_views.profile_view),
    path('@<profile_id>',public_views.profile_view),
]


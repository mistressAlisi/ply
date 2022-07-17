
from django.urls import path,include
from SLHUD import hud_views

urlpatterns = [
    path("",hud_views.hud_index),
    path('start/<uuid:parcel>/<uuid:agent>',hud_views.start),
    path('login/<uuid:parcel>/<uuid:agent>',hud_views.login),
    path("select/profile",hud_views.select_profile),
    path("select/profile/<uuid:profile>",hud_views.select_profile_activate)
]

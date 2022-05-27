
from django.urls import path,include
from SLHUD import hud_views

urlpatterns = [
    path('start/<uuid:parcel>/<uuid:agent>',hud_views.start)
]

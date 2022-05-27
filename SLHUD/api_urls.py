from django.urls import path,include
from SLHUD import api_views

urlpatterns = [
    path('update_agents/<uuid:parcel>',api_views.update_agents),
    path('rolls/action/',api_views.action_roll),
]


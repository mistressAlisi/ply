from django.urls import path,include
from plydice import api_views

urlpatterns = [
    path('roll/generic/<int:count>d<int:sides>',api_views.generic_roll),
]

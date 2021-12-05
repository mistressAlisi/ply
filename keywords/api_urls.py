from django.urls import path,include
from keywords import api_views

urlpatterns = [
    path('get/<search_str>',api_views.get_keywords),
    path('get/',api_views.get_keywords_all)    
]


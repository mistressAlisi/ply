from django.urls import path,include
from gallery import public_views
import ply
urlpatterns = [
    path('index',public_views.gallery_home)
    
]

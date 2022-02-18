from django.urls import path,include
from forge import user_views
urlpatterns = [
    path('create/profile/',user_views.create_profile),
    path('create/profile/preview/',user_views.create_profile_preview)    
]

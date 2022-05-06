from django.urls import path,include
from forge import user_views
urlpatterns = [
    path('select/profile/',user_views.select_profile),    
    path('create/profile/',user_views.create_profile),
    path('create/profile/preview/',user_views.create_profile_preview),
    path('edit/profile/',user_views.edit_profile),
    path('edit/profile/preview/',user_views.edit_profile_preview)
]

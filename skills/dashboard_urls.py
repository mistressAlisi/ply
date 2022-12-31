from django.urls import path,include
from skills import dashboard_views

urlpatterns = [
    path('all',dashboard_views.all_skills)
    #path('mentions',dashboard_views.all_mentions)
    #path('upload',dashboard_views.upload_content),
    #path('api/',include('gallery.api_urls')),
    #path('upload/lighttable/',dashboard_views.upload_lighttable)
]

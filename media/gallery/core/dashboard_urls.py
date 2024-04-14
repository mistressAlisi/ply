from django.urls import path,include
from media.gallery.core import dashboard_views

urlpatterns = [
    path('list', dashboard_views.gallery_list),
    path('likes', dashboard_views.gallery_myfavs),
    path('collections', dashboard_views.gallery_collections),
    path('manage', dashboard_views.gallery_manage),
    path('upload', dashboard_views.upload_content),
    path('api/',include('media.gallery.core.api_urls')),
    path('upload/lighttable/', dashboard_views.upload_lighttable)
]

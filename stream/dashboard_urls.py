from django.urls import path,include
from stream import dashboard_views

urlpatterns = [
    path('self',dashboard_views.profile_stream),
    path('view',dashboard_views.view_stream),
    path('create',dashboard_views.create_stream),
    path('api/',include('stream.dashboard_api_urls')),
    #path('upload/lighttable/',dashboard_views.upload_lighttable)
]

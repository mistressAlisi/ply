from django.urls import path,include
from communities.stream import dashboard_views

urlpatterns = [
    path('self', dashboard_views.profile_stream),
    path('view', dashboard_views.view_stream),
    path('create', dashboard_views.create_stream),
    path('configure/xmpp', dashboard_views.configure_xmpp),
    path('configure/xmpp/streams', dashboard_views.configure_stream_xmpp_integration),
    path('api/',include('communities.stream.dashboard_api_urls')),
    #path('upload/lighttable/',dashboard_views.upload_lighttable)
]

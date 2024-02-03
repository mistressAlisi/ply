from django.urls import path,include
from . import forge_views as views

urlpatterns = [
    path('config/xmpp',views.configure_xmpp,name="Configure XMPP Streams")
]

from django.urls import path,include
from . import forge_api_views as views

urlpatterns = [
 path("config/xmpp/submit",views.config_xmpp,name='Config XMPP')
]

from django.urls import path, include
from core.dynapages import api_views

urlpatterns = [
    path("setup/widget/<slug:widget_id>/<slug:mode>", api_views.widget_setup),
    # Api V1: static definitions of the dynapage node in the code
    path("factory/widget/<slug:widget_id>/<slug:mode>", api_views.widget_factory),
    path("setup/save_widget", api_views.widget_setup_factory),
    # Api V2: Dynapages Api V2 requires the parent page uuid to be specified in the URL:
    path("factory/widget/<uuid:page_uuid>/<slug:widget_id>/<slug:mode>", api_views.widget_factory_v2),
    path("setup/save_widget/<uuid:page_uuid>", api_views.widget_setup_factory_v2),
]

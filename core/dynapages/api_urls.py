from django.urls import path,include
from core.dynapages import api_views

urlpatterns = [
    path('factory/widget/<slug:widget_id>/<slug:mode>', api_views.widget_factory),
    path('setup/widget/<slug:widget_id>/<slug:mode>', api_views.widget_setup),
    path('setup/save_widget', api_views.widget_setup_factory)
]

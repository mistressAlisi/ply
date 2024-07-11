from django.urls import path, include
from . import forge_api_views as views

urlpatterns = [
    path("studio/load/<uuid:dashboard>", views.load_dashboard),
    path("studio/widgets/load/<uuid:dashboard>",views.load_widgets_url)
]

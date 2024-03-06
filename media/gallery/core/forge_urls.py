from django.urls import path,include
from . import forge_views as views

urlpatterns = [
    path("setup",views.setup,name="Setup")
]

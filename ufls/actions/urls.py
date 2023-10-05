from django.urls import path
from .views import PatchApi

app_name = "actions"

urlpatterns = [
    path('update/<str:notification_id>/', PatchApi.as_view())
]
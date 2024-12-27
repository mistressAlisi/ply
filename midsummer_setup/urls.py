from django.urls import path

from midsummer_setup import views

urlpatterns = [
    path('', views.setup_base),
    path('wizard/', views.setup_step1)
]
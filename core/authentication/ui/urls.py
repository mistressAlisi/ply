from django.urls import path
from core.authentication.ui import views
from django.views.generic import RedirectView
urlpatterns = [
    path('profile',RedirectView.as_view(url="/forge/select/profile")),
    path('profile/',RedirectView.as_view(url="/forge/select/profile")),
    path('login', views.login),
    path('login/', views.login),
    path('register', views.register),
    path('register/', views.register),
]

from django.urls import path
from . import views

app_name = "django_auth_oidc"

urlpatterns = [
	path('', views.login, name='login'),
	path('done/', views.callback, name='login-done'),
	path('logout/', views.logout, name='logout'),
]

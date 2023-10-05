from django.urls import path,include
from . import views

app_name="foauth"

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('local/', views.localLogin, name='local-login'),
    path('local/register/', views.localRegister, name='local-register'),
    path('local/forgot/', views.localForgot, name='local-forgot'),
    path('apps/', views.apps, name='apps'),
    path('oauth/', views.oauthLogin, name='oauth-login'),
    path('oauth/return/', views.oauthReturn, name='oauth-return'),
]

from django.urls import path,include
from .my import views

app_name="account"

urlpatterns = [
    path('my/registrations/', views.getMyRegistrations),
    path('my/registrations/uploadImage/<str:orderDisplayId>/', views.uploadNewImageTwentyTwo),
    path('my/registrations/associate/<str:orderDisplayId>/', views.associateNewId),
    path('my/registrations/associate-validation/<str:key>/', views.associateNewIdEmailVerification),
]

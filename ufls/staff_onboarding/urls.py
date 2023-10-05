from django.contrib.auth import views as auth_views
from django.urls import include, path

from staff_onboarding import views

app_name = "onboarding"

urlpatterns = [
    path("convert/<str:applicationRecord>/", views.appConvert, name="convert"),
    path("mark/<str:applicationRecord>/", views.appMark, name="mark"),
    path("decline/<str:applicationRecord>/", views.appDecline, name="decline"),
    path("setup/<str:onboardRecord>/", views.commitChanges, name="setup"),
    path("del/<str:onboardRecord>/", views.deleteRecord, name="delete-record"),
    path("begin/authorize/", views.startAuthorize, name="start-authorize"),
    path("return/authorize/", views.returnAuthorize, name="return-authorize"),
]

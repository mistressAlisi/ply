from django.urls import path,include
from communities.profiles import dashboard_views

urlpatterns = [
    path('current',dashboard_views.profile_view),
]

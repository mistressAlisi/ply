from django.urls import path,include
from community import api_views
import ply
urlpatterns = [
    path('friend/remove/<int:rmf>',api_views.remove_friend)

]


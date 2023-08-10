from django.urls import path,include
from communities.community import api_views
import ply
urlpatterns = [
    path('friend/remove/<int:rmf>',api_views.remove_friend),
    path('follow/<uuid:target>',api_views.follow_profile),
    path('friend/<uuid:target>',api_views.add_friend),
    path('unfriend/<uuid:target>',api_views.un_friend),
    path('unfollow/<uuid:target>',api_views.unfollow_profile)
]


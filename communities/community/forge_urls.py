from django.urls import path
from communities.community import forge_views

urlpatterns = [
    path("staff", forge_views.community_staff),
    path("admins", forge_views.community_admins),
    path("menus/editor", forge_views.sidebar_menu_editor),
    path("profile/editor", forge_views.default_profile_editor),
]

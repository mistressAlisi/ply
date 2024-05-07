from django.urls import path
from communities.community import forge_api_views

urlpatterns = [
    path("staff/create", forge_api_views.create_community_staff),
    path("staff/delete/<uuid:staff>", forge_api_views.delete_community_staff),
    path("admin/create", forge_api_views.create_community_admin),
    path("admin/delete/<uuid:staff>", forge_api_views.delete_community_admin),
    path("menu/create", forge_api_views.create_community_sidebar_menu),
    path("menu/edit/<uuid:menu>", forge_api_views.get_community_sidebar_menu),
    path("menu/delete/<uuid:menu>", forge_api_views.del_community_sidebar_menu)
]

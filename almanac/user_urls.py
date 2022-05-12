from django.urls import path,include
from almanac import user_views
urlpatterns = [
    path('page/create',user_views.create_page),
    path('page/create/preview',user_views.create_page_preview),
    path('page/create/commit',user_views.create_page_commit),
    path('page/edit/<slug:page_id>',user_views.edit_page),
    path('menu/editor',user_views.edit_menu),
    #path('/menu/add',user_views.add_page2menu),
    #path('/menu/editor',user_views.menu_editor)
]

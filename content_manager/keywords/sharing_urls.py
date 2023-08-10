from django.urls import path
from content_manager.keywords import sharing_views

urlpatterns = [
    path('<slug:keyword_search>', sharing_views.keyword_share_search_view)

]


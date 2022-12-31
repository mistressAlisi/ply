from django.urls import path,include
from keywords import sharing_views
import ply
urlpatterns = [
    path('<slug:keyword_search>',sharing_views.keyword_share_search_view)

]


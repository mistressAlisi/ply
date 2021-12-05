from django.urls import path,include
from dashboard import user_views
import ply
urlpatterns = [
    path('',user_views.dashboard_home)
]
# Dynamic Module loading also means Dynamic Path generation. 
# CAVEAT, NOTE: ANY module that is defined in PLY_USER_DASHBOARD_MODULES must include a dashboard_urls class even if it's empty.
for mname in ply.settings.PLY_USER_DASHBOARD_MODULES:
    urlpatterns.append(path(f"{mname}/",include(f"{mname}.dashboard_urls")))

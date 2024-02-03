from django.urls import path,include
from dashboard import staff_views
import ply
urlpatterns = [
    path('',staff_views.dashboard_home),
    path('dashboard_panel_home',staff_views.dashboard_panel_home)
]
# Dynamic Module loading also means Dynamic Path generation. 
# CAVEAT, NOTE: ANY module that is defined in PLY_STAFF_DASHBOARD_MODULES must include a forge_urls class even if it's empty.
for mname in ply.settings.PLY_STAFF_DASHBOARD_MODULES:
    urlpatterns.append(path(f"{mname}/",include(f"{mname}.forge_urls")))

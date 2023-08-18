from django.urls import path,include
from dashboard import forge_views
import ply
urlpatterns = [
    path('',forge_views.dashboard_home),
    path('forge/',include('core.forge.urls'))
]
# Dynamic Module loading also means Dynamic Path generation. 
# CAVEAT, NOTE: ANY module that is defined in PLY_USER_DASHBOARD_MODULES must include a dashboard_urls class even if it's empty.
for mname in ply.settings.PLY_USER_DASHBOARD_MODULES:
    urlpatterns.append(path(f"{mname}/",include(f"{mname}.forge_urls")))

from django.urls import path,include
from dashboard import forge_views
import ply
from ply import settings
from ply.toolkit.core import get_ply_appinfo
from ply.toolkit.logger import getLogger

logging = getLogger("dashboard", name="forge_urls")
urlpatterns = [
    path('',forge_views.dashboard_home),
    path('dashboard_panel_home',forge_views.dashboard_panel_home),
    path('forge/',include('core.forge.urls'))
]
# Dynamic Module loading also means Dynamic Path generation. 
# CAVEAT, NOTE: ANY module that is defined in PLY_WORLDFORGE_DASHBOARD_MODULES  or Dynamically below must include the forge_urls and forge_api_urls classes even if it empty.
for mname in settings.PLY_WORLDFORGE_DASHBOARD_MODULES:
    urlpatterns.append(path(f"api/{mname}/",include(f"{mname}.forge_api_urls")))
    urlpatterns.append(path(f"{mname}/", include(f"{mname}.forge_urls")))

# Now we also support *dynamic* url building using the ply_appinfo APIs:
if settings.PLY_DYNAMIC_APP_URLS_ENABLED:
    logging.info("Dynamic Forge URL-path builder is enabled by settings.PLY_DYNAMIC_APP_URLS_ENABLED!")
    assigned = []
    for app in settings.INSTALLED_APPS:
        app_data = get_ply_appinfo(app)
        if app_data:
            if "dashboard_modes" in app_data.PLY_APP_INFO:
                if "forge" in app_data.PLY_APP_INFO["dashboard_modes"]:
                    if app_data.PLY_APP_INFO["dashboard_modes"]["forge"]["active"]:
                        if app_data.PLY_APP_INFO['app_module'] not in settings.PLY_WORLDFORGE_DASHBOARD_MODULES:
                            logging.info(f"Forge: Adding Module {app_data.PLY_APP_INFO['app_module']} to url paths...")
                            urlpatterns.append(path(f"api/{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.forge_api_urls")))
                            urlpatterns.append(path(f"{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.forge_urls")))
                        else:
                            logging.info(f"Forge: Module {app_data.PLY_APP_INFO['app_module']} is defined in settings.PLY_WORLDFORGE_DASHBOARD_MODULES: Not Loading dynamically again.")

    logging.info("Forge: URL Path generation complete!")
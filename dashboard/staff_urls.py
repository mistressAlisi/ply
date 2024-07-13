from django.urls import path, include
from dashboard import staff_views
import ply
from ply import settings
from ply.toolkit.core import get_ply_appinfo
from ply.toolkit.logger import getLogger

logging = getLogger("dashboard", name="staff_urls")
urlpatterns = [
    path("", staff_views.dashboard_home),
    path("dashboard_panel_home", staff_views.dashboard_panel_home),
]
# Dynamic Module loading also means Dynamic Path generation.
# CAVEAT, NOTE: ANY module that is defined in PLY_STAFF_DASHBOARD_MODULES must include a forge_urls class even if it's empty.
for mname in ply.settings.PLY_STAFF_DASHBOARD_MODULES:
    urlpatterns.append(path(f"api/{mname}/", include(f"{mname}.staff_api_urls")))
    urlpatterns.append(path(f"{mname}/", include(f"{mname}.staff_urls")))

# Now we also support *dynamic* url building using the ply_appinfo APIs:
if settings.PLY_DYNAMIC_APP_URLS_ENABLED:
    logging.info("Dynamic Staff URL-path builder is enabled by settings.PLY_DYNAMIC_APP_URLS_ENABLED!")
    assigned = []
    for app in settings.INSTALLED_APPS:
        app_data = get_ply_appinfo(app)
        if app_data:
            if "dashboard_modes" in app_data.PLY_APP_INFO:
                if "staff" in app_data.PLY_APP_INFO["dashboard_modes"]:
                    if app_data.PLY_APP_INFO["dashboard_modes"]["staff"]["active"]:
                        if app_data.PLY_APP_INFO['app_module'] not in settings.PLY_STAFF_DASHBOARD_MODULES:
                            logging.info(f"Staff: Adding Module {app_data.PLY_APP_INFO['app_module']} to url paths...")
                            urlpatterns.append(path(f"api/{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.staff_api_urls")))
                            urlpatterns.append(path(f"{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.staff_urls")))
                        else:
                            logging.info(f"Staff: Module {app_data.PLY_APP_INFO['app_module']} is defined in settings.PLY_STAFF_DASHBOARD_MODULES: Not Loading dynamically again.")

    logging.info("Staff: URL Path generation complete!")
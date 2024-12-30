from django.urls import path,include
from dashboard import user_views
import ply
from django.conf import settings
from ply.toolkit.core import get_ply_appinfo
from ply.toolkit.logger import getLogger

logging = getLogger("dashboard", name="user_urls")
urlpatterns = [
    path('',user_views.dashboard_home),
    path('set_profile/<uuid:puuid>',user_views.dashboard_profile_switch)
]
# Dynamic Module loading also means Dynamic Path generation. 
# CAVEAT, NOTE: ANY module that is defined in PLY_USER_DASHBOARD_MODULES must include a dashboard_urls class even if it's empty.
for mname in settings.PLY_USER_DASHBOARD_MODULES:
    try:
        urlpatterns.append(path(f"api/{mname}/", include(f"{mname}.dashboard_api_urls")))
    except Exception as e:
        logging.error(f"Unable to Add App to path: {mname}.dashboard_api_urls:",e)
    try:
        urlpatterns.append(path(f"{mname}/",include(f"{mname}.dashboard_urls")))
    except Exception as e:
        logging.error(f"Unable to Add App to path: {mname}.dashboard_urls:", e)
# Now we also support *dynamic* url building using the ply_appinfo APIs:
if settings.PLY_DYNAMIC_APP_URLS_ENABLED:
    logging.info("Dynamic User URL-path builder is enabled by settings.PLY_DYNAMIC_APP_URLS_ENABLED!")
    assigned = []
    for app in settings.INSTALLED_APPS:
        app_data = get_ply_appinfo(app)
        if app_data:
            if "dashboard_modes" in app_data.PLY_APP_INFO:
                if "user" in app_data.PLY_APP_INFO["dashboard_modes"]:
                    if app_data.PLY_APP_INFO["dashboard_modes"]["user"]["active"]:
                        if app_data.PLY_APP_INFO['app_module'] not in settings.PLY_USER_DASHBOARD_MODULES:
                            logging.info(f"User: Adding Module {app_data.PLY_APP_INFO['app_module']} to url paths...")
                            try:
                                urlpatterns.append(path(f"api/{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.dashboard_api_urls")))
                            except Exception as e:
                                logging.error(f"Unable to Add App to path: {app_data.PLY_APP_INFO['app_module']}.dashboard_api_urls", e)
                            try:
                                urlpatterns.append(path(f"{app_data.PLY_APP_INFO['app_module']}/", include(f"{app_data.PLY_APP_INFO['app_module']}.dashboard_urls")))
                            except Exception as e:
                                logging.error(f"Unable to Add App to path: {app_data.PLY_APP_INFO['app_module']}.dashboard_urls", e)
                        else:
                            logging.info(f"User: Module {app_data.PLY_APP_INFO['app_module']} is defined in settings.PLY_USER_DASHBOARD_MODULES: Not Loading dynamically again.")

    logging.info("User: URL Path generation complete!")
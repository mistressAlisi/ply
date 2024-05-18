import datetime
from django import template
from ply.toolkit import community
from ply.toolkit.core import get_ply_appinfo

register = template.Library()


@register.simple_tag()
def get_sidebar_menu_ctrl(app, mode):
    app_info = get_ply_appinfo(app)
    if app_info is None:
        return f"Module {app}.ply_appinfo not found."
    if mode not in app_info.PLY_APP_INFO["dashboard_modes"]:
        return f"N/A"
    else:
        if app_info.PLY_APP_INFO["dashboard_modes"][mode]["active"]:
            return f"Active"
        else:
            return f"N/A"
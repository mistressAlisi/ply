"""
toolkit/themes.py
====================================
Toolkit utilities for interacting with Ply's Theme System
"""
import importlib
from ply.toolkit.logger import getLogger
from ply import settings
logging = getLogger('toolkit.themes',name='toolkit.themes')



def get_theme_info(theme_name):
    """
    Get the info module for a given theme and return it. This basically just wraps around importlib.
    @param theme_name: Theme module name to import. This is the path we'll pass to importlib. The theme module must at least implement theme.py.
    @return: the chosen theme's Info module.
    """
    try:
        theme_class = importlib.import_module(f'{theme_name}.theme')
        return theme_class
    except Exception as e:
        logging.error(f"UNABLE TO LOAD THEME {theme_name} ERROR: {e}")
        raise Exception(f"Unable to load {theme_name} module, does {theme_name}.theme exist?")


def get_community_theme_or_def(community):
    """
    Get the communities' defined Theme (the actual module's theme.py info class) or the system default theme.
    The default is PLY_DEFAULT_THEME
    @param community: Community to check for theme
    @return: Theme info class (theme.py) for the given module (app name) or default if none.
    """
    if community.theme:
        return get_theme_info(community.theme)
    else:
        return get_theme_info(settings.PLY_DEFAULT_THEME)

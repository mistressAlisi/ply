# The PLY Appinfo class defines ply-specific details for the given application.
PLY_APP_INFO = {
    "app_name": "Example App",
    "app_module": "communities.example",
    "version": {
        "release":2024,
        "major":0x7e8,
        "minor":0x3e9
    },
    "required_versions": {
        "featureset_major": 0x7e8,
        "featureset_minor": 0x3e9,
    },

    "dashboard_modes": {
        "user":{
            "privileged": False,
            "default": True,
            "active": True,
            "descr": "The default user dashboard!",
            "menu_class": "sidebar_menu",
        },
        "forge":{
            "privileged": True,
            "default": False,
            "active": True,
            "descr": "The WorldForge/World admin dashboard mode",
            "menu_class": "sidebar_forge",
        },
        #"staff": {
        #     "privileged": True,
        #     "default": False,
        #     "active": False,
        #     "descr": "The Staff dashboard mode",
        #     "menu_class": "sidebar_staff",
        # },
    },
    "app_endpoints": {
        "registrar": {
            "url_base":"the/url/path/ after /app",
            "module":"some_url_file_relative_to_module.py",
            "enable": False

        }
    }
}

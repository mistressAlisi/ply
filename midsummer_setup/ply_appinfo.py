# The PLY Appinfo class defines ply-specific details for the given application.
PLY_APP_INFO = {
    "app_name": "Midsummer Setup",
    "app_module": "midsummer_setup",
    "version": {
        "release":2024,
        "major":0x7e8,
        "minor":0x3e9
    },
    "required_versions": {
        "featureset_major": 0x7e8,
        "featureset_minor": 0x3e9,
    },
    "app_endpoints": {
        "setup": {
            "url_base": "setup",
            "module": "midsummer_setup.urls",
            "enable": True,
        }
    },
}

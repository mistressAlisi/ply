"""
toolkit/core.py
====================================
Toolkit utilities for interacting with Core system APIs (Apps and Modules):
"""
import importlib


def get_ply_appinfo(app):
    try:
        app_spec = importlib.import_module(f"{app}.ply_appinfo")
    except ImportError:
        return None
    return app_spec
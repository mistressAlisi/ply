"""
toolkit/version.py
====================================
Toolkit utilities for Getting the Plysystem version
"""
import io
from core import version


def get_featureset_version():
    return version.PLY_VERSION_FEATURESET_MAJOR, version.PLY_VERSION_FEATURESET_MINOR, str(version.PLY_VERSION_FEATURESET_MAJOR)+"."+str(version.PLY_VERSION_FEATURESET_MINOR)


def get_version_str():
    return str(version.PLY_VERSION_MAJOR)+"."+str(version.PLY_VERSION_MINOR)+"."+version.PLY_VERSION_MINOR_CODE+":"+version.PLY_VERSION_MINOR_PATCH

def get_version():
    return version
def is_dev_version():
    return version.PLY_VERSION_DEV
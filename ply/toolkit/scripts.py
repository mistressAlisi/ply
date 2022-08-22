"""
toolkit/scripts.py
====================================
Toolkit utilities for interacting with Plyscripts
"""
import io
from contextlib import redirect_stdout
from community.models import Community,VHost
from plyscript.models import Script,ScriptRegistry
from ply.toolkit.logger import getLogger
from profiles.models import Profile
from preferences.models import Preferences
from community.models import ProfilePerCoummunityView

def exec_script_str(community,profile,code_body):
    globals = {'community':community,'profile':profile,'pref':Preferences.objects.get(user=profile.creator)}
    fe_o = io.StringIO()
    with redirect_stdout(fe_o):
        ret_data = exec(code_body, {"built" : __builtins__},globals)
    ret = fe_o.getvalue()
    return ret

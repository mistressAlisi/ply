"""
toolkit/scripts.py
====================================
Toolkit utilities for interacting with Plyscripts
"""
import io
from contextlib import redirect_stdout
from communities.preferences.models import Preferences


def exec_script_str(community,profile,code_body):
    globals = {'community':community,'profile':profile,'pref':Preferences.objects.get_or_create(user=profile.creator)[0]}
    fe_o = io.StringIO()
    with redirect_stdout(fe_o):
        ret_data = exec(code_body, {"built" : __builtins__},globals)
    ret = fe_o.getvalue()
    return ret


def exec_script(script_obj,profile,community):
    globals = {'community':community,'profile':profile,'pref':Preferences.objects.get_or_create(user=profile.creator)[0],'__function_name__':script_obj.function_name}
    fe_o = io.StringIO()
    with redirect_stdout(fe_o):
        code_body = script_obj.body
        ret_data = exec(code_body, {"built" : __builtins__},globals)
    ret = fe_o.getvalue()
    return ret

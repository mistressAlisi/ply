"""
toolkit/responses.py
====================================
Toolkit helpers for quickly generating responses compliant with Dashboard API applications :)
"""
from django.http import JsonResponse


def notice_response(msg="This is a Notice!"):
    return JsonResponse(
        {
            "res": "notice",
            "msg": msg
        },
        safe=False,
    )

def generic_error_response(err_class="Error",err_msg="Error Text!!"):
    return JsonResponse({"res": "err", "e": {err_class: [err_msg]}}, safe=False)

def generic_success():
    return JsonResponse(
        {
            "res": "ok",
        },
        safe=False,
    )

def form_errors(error_obj):
    return JsonResponse({"res": "err", "e": error_obj}, safe=False)
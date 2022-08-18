import json

import importlib
from django.shortcuts import render
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction



import ply
from preferences.models import Preferences
from preferences.forms import PreferencesForm

@login_required
@transaction.atomic
def save_system_settings(request):
    uprefs = Preferences.objects.get_or_create(user=request.user)[0]
    form_saver = PreferencesForm(request.POST,instance=prefs)
    if (not form_saver.is_valid()):
        return JsonResponse({"res":"err","e":str(form_saver.errors.as_data())},safe=False)
    form_saver.save()
    return JsonResponse("ok",safe=False)

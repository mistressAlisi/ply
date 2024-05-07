"""
toolkit/preferences.py
====================================
Toolkit utilities for interacting with Preferences Objects:
"""
from communities.preferences.models import Preferences


def get_user_preferences(request):
    preferences = Preferences.objects.get_or_create(user=request.user)
    if preferences[1] == 1:
        preferences[0].save()
    return preferences[0]
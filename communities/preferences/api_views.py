from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction

from communities.preferences.models import Preferences
from communities.preferences.forms import PreferencesForm

@login_required
@transaction.atomic
def save_system_settings(request):
    uprefs = Preferences.objects.get_or_create(user=request.user)[0]
    form_saver = PreferencesForm(request.POST,instance=uprefs)
    if (not form_saver.is_valid()):
        return JsonResponse({"res":"err","e":str(form_saver.errors.as_data())},safe=False)
    form_saver.save()
    return JsonResponse({"res":"ok"},safe=False)

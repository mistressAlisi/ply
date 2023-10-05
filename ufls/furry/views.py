from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

from connections.models import Application
from .models import EmailValidation
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import PasswordChangeForm

# Create your views here.
def verify(request, username, key):
    user = get_object_or_404(User, username=username.lower())
    key = get_object_or_404(EmailValidation, key=key, user=user)
    user.is_active = True
    user.save()
    login(request, user)

    if(request.GET.get('from', None) != None):
        return redirect('launch_scoping_r', key=request.GET.get('from', ''), rapid=True)

    return render(request, 'redir_login.html', context={})

def newPassword(request, username, key):
    if(request.method == "POST" and request.user.is_active):
        form = PasswordChangeForm(request.POST)
        if(form.is_valid()):
            user = get_object_or_404(User, username=request.user.username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            key = get_object_or_404(EmailValidation, key=key, user=user, used=False)
            key.used = True
            key.save()
            return redirect(reverse("foauth:index") + "?err=reset-done&from="+request.GET.get('from', ''))
    user = get_object_or_404(User, username=username.lower())
    login(request, user)
    form = PasswordChangeForm()
    return render(request, 'new_password_form.html', context={"user": user, "form": form})


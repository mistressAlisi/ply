from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from ply.toolkit import vhosts,themes


# Create your views here.

def login(request):
    vhost,community = vhosts.get_vhost_and_community(request)
    theme = themes.get_community_theme_or_def(community)
    af = AuthenticationForm()
    context = {'form':af,'community':community,'THEME_PATH':theme.THEME_PATH}
    return render(request,"authentication/registration/login.html",context)

def register(request):
    vhost,community = vhosts.get_vhost_and_community(request)
    theme = themes.get_community_theme_or_def(community)
    af = UserCreationForm()
    context = {'form':af,'community':community,'THEME_PATH':theme.THEME_PATH}
    return render(request,"django_registration/registration_form.html",context)
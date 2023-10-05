import os

import requests
from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from django_auth_oidc.auth import get_server
from django_auth_oidc.views import LoginFailed, _import_object
from connections.models import Application
from furry.models import Profile, EmailValidation
from ufls import settings

try:
    LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
except AttributeError:
    LOGIN_REDIRECT_URL = '/connect/'

try:
    LOGOUT_REDIRECT_URL = settings.LOGOUT_REDIRECT_URL
except AttributeError:
    LOGOUT_REDIRECT_URL = '/connect/logout/'

try:
    AUTH_SCOPE = settings.AUTH_SCOPE
except AttributeError:
    AUTH_SCOPE = ('openid',)

try:
    GET_USER_FUNCTION = settings.AUTH_GET_USER_FUNCTION
except AttributeError:
    GET_USER_FUNCTION = 'django_auth_oidc:get_user_by_username'

try:
    ALLOWED_REDIRECTION_HOSTS = [host for host in os.getenv('ALLOWED_REDIRECTION_HOSTS', '').split(',') if
                                 host] or settings.ALLOWED_REDIRECTION_HOSTS
except AttributeError:
    ALLOWED_REDIRECTION_HOSTS = []

get_user = _import_object(GET_USER_FUNCTION, 'get_user')

# Create your views here.

def index(request):
    request.session['storage_oauth_snapshot'] = request.GET

    connecting_from = {"valid": False, "app_name": ""}

    err = request.GET.get('error', None)

    try:
        if(request.session['storage_oauth_snapshot']['from'] != None):
            connecting_from['valid'] = True
            connecting_from['app_name'] = Application.objects.filter(code=request.session['storage_oauth_snapshot']['from']).first()
            if (connecting_from['app_name'] == None):
                connecting_from['valid'] = False
            else:
                if request.user.is_authenticated and request.user.is_active:
                    if(request.GET.get('rapid',None) != None):
                        return redirect('launch_scoping_r', key=connecting_from['app_name'].code, rapid=True)
                    return redirect('launch_scoping', key=connecting_from['app_name'].code)
    except KeyError:
        pass

    if (request.method == 'POST'):
        email = request.POST['username'].lower()
        if (email.find("@furrydelphia.org") != -1 or email.find("@staff.furrydelphia.org") != -1):
            return redirect(reverse("foauth:oauth-login") + '?email=%s' % email)

        lookup = get_user_model().objects.filter(email=email).first()
        if (lookup == None):
            return redirect(reverse("foauth:local-register") + '?email=%s' % email)

        return redirect(reverse("foauth:local-login") + '?email=%s' % email)

    return render(request, 'email_capture.html', {"connecting": connecting_from, "err": err})


def localLogin(request):
    eml = request.GET.get('email', None)
    connecting_from = {"valid": False, "app_name": ""}

    try:
        if(request.session['storage_oauth_snapshot']['from'] != None):
            connecting_from['valid'] = True
            connecting_from['app_name'] = Application.objects.filter(code=request.session['storage_oauth_snapshot']['from']).first()
            if (connecting_from['app_name'] == None):
                connecting_from['valid'] = False
            else:
                if request.user.is_authenticated and request.user.is_active:
                    if (connecting_from['valid'] == True):
                        return redirect('foauth:apps')
                    else:
                        return redirect('launch_scoping', key=connecting_from['app_name'].code)
    except KeyError:
        pass

    err = None

    if(request.method == 'POST'):
        pn = request.POST
        email = eml
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if (connecting_from['valid'] == True):
                    return redirect('launch_scoping_r', key=connecting_from['app_name'].code, rapid=True)
                else:
                    return redirect('foauth:apps')
            else:
                err = "Your account is not active. Please check your e-mail for an activation link."
        else:
            err = "Invalid username or password"


    return render(request, 'local_login.html', {"eml": eml, "connecting": connecting_from, "err": err})


def determineFrom(connecting_from):
    if(connecting_from['valid'] == True):
        return connecting_from['app_name'].code
    return ""

def localRegister(request):
    eml = request.GET.get('email', None)
    connecting_from = {"valid": False, "app_name": ""}

    try:
        if(request.session['storage_oauth_snapshot']['from'] != None):
            connecting_from['valid'] = True
            connecting_from['app_name'] = Application.objects.filter(code=request.session['storage_oauth_snapshot']['from']).first()
            if (connecting_from['app_name'] == None):
                connecting_from['valid'] = False
            else:
                if request.user.is_authenticated and request.user.is_active:
                    if (connecting_from['valid'] == True):
                        return redirect('launch_scoping', key=connecting_from['app_name'].code)
                    else:
                        return redirect('foauth:apps')

    except KeyError:
        pass

    if(request.method == 'POST'):
        pn = request.POST
        email = eml
        password = request.POST['password']
        user = get_user_model().objects.create_user(username=email.lower(), email=email.lower(), password=password)
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user)
        email = EmailValidation.objects.create(
            user=user,
            usedFor='verification.email.firstCreate'
        )
        # todo: email
        send_mail(
            'Furrydelphia UFLS - Verify your E-mail',
            'Please click the following link to verify your account creation at Furrydelphia. If you did not request this, you can safely ignore this message. https://backend.furrydelphia.org/verify/%s/%s/?from=%s' % (
            user.email, email.key, determineFrom(connecting_from)),
            'bots@furrydelphia.org',
            [user.email],
            fail_silently=False
        )
        connecting_from['valid'] = False
        return render(request, 'email_verify.html', {"eml": eml, "connecting": connecting_from})

    return render(request, 'local_register.html', {"eml": eml, "connecting": connecting_from})


def oauthLogin(request, return_path=None):
    if return_path is None:
        return_path = request.GET.get(auth.REDIRECT_FIELD_NAME, "")

    request.session['login_attempt'] = request.session.get('login_attempt', 0) + 1

    email = request.GET.get('email', None)

    return redirect(get_server().authorize(
        redirect_uri=request.build_absolute_uri(reverse("foauth:oauth-return")),
        state=return_path,
        scope=AUTH_SCOPE,
    ) + "&login_hint=%s" % email)


def login_again(request, return_path=None):
    if request.session.get('login_attempt', 5) < 3:
        return oauthLogin(request, return_path)
    else:
        raise LoginFailed(f"Login failed after trying {request.session.get('login_attempt')} times.")


def oauthReturn(request):
    return_path = request.GET.get("state")
    code = request.GET.get("code")

    if not code:
        return login_again(request, return_path, custom_id=None)
    res = get_server().request_token(
        redirect_uri='https://backend.furrydelphia.org/connect/oauth/return/',
        code=request.GET["code"],
    )
    user = get_user(res.id)
    auth.login(request, user)

    if(user.is_active == False):
        #thing
        pass

    request.session['openid_token'] = res.id_token
    request.session['openid'] = res.id

    connecting_from = {"valid": False, "app_name": ""}
    try:
        if (request.session['storage_oauth_snapshot']['from'] != None):
            connecting_from['valid'] = True
            connecting_from['app_name'] = Application.objects.filter(
                code=request.session['storage_oauth_snapshot']['from']).first()
            if (connecting_from['app_name'] == None):
                connecting_from['valid'] = False
    except KeyError:
        pass
    if(connecting_from['valid'] == True):
        return redirect('launch_scoping_r', key=connecting_from['app_name'].code, rapid=True)
    else:
        return redirect('foauth:apps')


def logout(request):
    auth.logout(request)
    return redirect(reverse("foauth:index") + '?from=%s' % request.GET.get('from', None))


def localForgot(request):
    email = request.GET.get('email', None)
    if (email.find("@furrydelphia.org") != -1 or email.find("@staff.furrydelphia.org") != -1):
        return redirect(reverse("foauth:index") + '?err=cannot-reset-staff-oauth')

    lookup = get_user_model().objects.filter(email=email).first()
    if (lookup != None):
        email = EmailValidation.objects.create(
            user=lookup,
            usedFor='verification.account.resetPassword'
        )
        # todo: email
        send_mail(
            'Furrydelphia UFLS - Password Reset Request',
            'Someone (hopefully you) has requested a Password Reset for your Furrydelphia UFLS account. If you did not request this, you can safely ignore this message. https://backend.furrydelphia.org/newPassword/%s/%s/?from=%s' % (
                lookup.email, email.key, request.GET.get('from', None)),
            'bots@furrydelphia.org',
            [lookup.email],
            fail_silently=False
        )

    return redirect(reverse("foauth:index") + '?err=reset-sent')

def checkStaffEligible(email):
    r = requests.get("https://staff.furrydelphia.org/api/staff/%s/" % email, headers={"Authorization": "Token %s" % ("7d2c55e35dcddfed445218e9081831755553dcbd")})
    n = r.json()
    if(len(n) == 0):
        return False
    else:
        return True

@login_required(login_url='/connect/')
def apps(request):
    apps = Application.objects.filter(enabled=True, show_on_app_list=True)
    if(checkStaffEligible(request.user.username) == False):
        apps = apps.filter(staff_only=False)
    return render(request, 'app_select.html', {"apps": apps})


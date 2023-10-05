import os

from importlib import import_module

from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
#from django.utils.http import is_safe_url

from .auth import get_server

try:
	LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
except AttributeError:
	LOGIN_REDIRECT_URL = '/'

try:
	LOGOUT_REDIRECT_URL = settings.LOGOUT_REDIRECT_URL
except AttributeError:
	LOGOUT_REDIRECT_URL = '/'

try:
	AUTH_SCOPE = settings.AUTH_SCOPE
except AttributeError:
	AUTH_SCOPE = ('openid',)

try:
	GET_USER_FUNCTION = settings.AUTH_GET_USER_FUNCTION
except AttributeError:
	GET_USER_FUNCTION = 'django_auth_oidc:get_user_by_username'

try:
	ALLOWED_REDIRECTION_HOSTS = [host for host in os.getenv('ALLOWED_REDIRECTION_HOSTS', '').split(',') if host] or settings.ALLOWED_REDIRECTION_HOSTS
except AttributeError:
	ALLOWED_REDIRECTION_HOSTS = []


def _import_object(path, def_name):
	try:
		mod, cls = path.split(':', 1)
	except ValueError:
		mod = path
		cls = def_name

	return getattr(import_module(mod), cls)

get_user = _import_object(GET_USER_FUNCTION, 'get_user')


def login(request, return_path = None):
	if return_path is None:
		return_path = request.GET.get(auth.REDIRECT_FIELD_NAME, "")

	request.session['login_attempt'] = request.session.get('login_attempt', 0) + 1

	return redirect(get_server().authorize(
		redirect_uri = request.build_absolute_uri(reverse("django_auth_oidc:login-done")),
		state = return_path,
		scope = AUTH_SCOPE,
	))


class LoginFailed(Exception):
	pass


def login_again(request, return_path = None):
	if request.session.get('login_attempt', 5) < 3:
		return login(request, return_path)
	else:
		raise LoginFailed(f"Login failed after trying {request.session.get('login_attempt')} times.")


def callback(request):
	return_path = request.GET.get("state")
	code = request.GET.get("code")

	if not code:
		return login_again(request, return_path)

	res = get_server().request_token(
		redirect_uri = request.build_absolute_uri(reverse("django_auth_oidc:login-done")),
		code = request.GET["code"],
	)

	user = get_user(res.id)
	if not user or not user.is_authenticated:
		return login_again(request, return_path)

	del request.session['login_attempt']
	auth.login(request, user)
	request.session['openid_token'] = res.id_token
	request.session['openid'] = res.id
	"""
	url_is_safe = is_safe_url(
		url = return_path,
		allowed_hosts = {request.get_host(), *ALLOWED_REDIRECTION_HOSTS},
	)
	if not url_is_safe:
		return redirect(resolve_url(LOGIN_REDIRECT_URL))
	"""
	return redirect(return_path)


def logout(request):
	id_token = request.session.get('openid_token', '')
	auth.logout(request)

	server = get_server()
	if server.end_session_endpoint:
		return redirect(server.end_session(
			post_logout_redirect_uri = request.build_absolute_uri(LOGOUT_REDIRECT_URL),
			state = '',
			id_token_hint = id_token,
		))
	else:
		return redirect(request.build_absolute_uri(LOGOUT_REDIRECT_URL))

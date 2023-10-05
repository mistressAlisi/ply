import django
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
django.setup()
from django.contrib.auth.models import AnonymousUser
#from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token=token_key, verify=True)
        u = get_user_model().objects.get(id=token.payload.get("user_id"))
        return u
    except TokenError:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
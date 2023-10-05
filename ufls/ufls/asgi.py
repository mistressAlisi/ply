"""
ASGI config for ufls project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from ufls.wsurls import websocket_urlpatterns
from ufls.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufls.settings')

os.environ['asgi.url_scheme'] = 'https'

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        TokenAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
})
from datetime import timedelta
import os
from time import time
from threading import Lock

from django.conf import settings

from openid_connect import connect, connect_url

server_cache = None
server_cache_lock = Lock()
server_cache_expires = None

def get_server():
	global server_cache, server_cache_expires, server_cache_lock

	with server_cache_lock:
		now = time()
		if not server_cache_expires or server_cache_expires <= now:
			AUTH_URL = os.environ.get("AUTH_URL")
			if AUTH_URL:
				server_cache = connect_url(AUTH_URL)
			else:
				server_cache = connect(settings.AUTH_SERVER, settings.AUTH_CLIENT_ID, settings.AUTH_CLIENT_SECRET, getattr(settings, 'AUTH_PROTOCOL', None))
			server_cache_expires = now + timedelta(hours=1).total_seconds()

		return server_cache

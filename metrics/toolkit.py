import ply
from ply.toolkit import vhosts,profiles
def request_data_capture(request,metricsObject):
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        metricsObject.visitor = profile
    if 'User-Agent' in request.headers:
        metricsObject.user_agent = request.headers["User-Agent"]
    if 'REMOTE_ADDR' in request.META:
        metricsObject.remote_addr = request.META["REMOTE_ADDR"]
    metricsObject.save()
    return True

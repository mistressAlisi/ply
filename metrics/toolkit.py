from profiles.models import Profile
def request_data_capture(request,metricsObject):
    if request.user.is_authenticated:
        metricsObject.visitor = Profile.objects.get(pk=request.session['profile'])
    if 'User-Agent' in request.headers:
        metricsObject.user_agent = request.headers["User-Agent"]
    if 'REMOTE_ADDR' in request.META:
        metricsObject.remote_addr = request.META["REMOTE_ADDR"]
    metricsObject.save()
    return True

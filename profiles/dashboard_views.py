from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

#PLY:
from dynapages import models as dynapages
import ply
from ply.toolkit import vhosts
from gallery.uploader import upload_plugins_builder
from profiles.models import Profile
from group.models import Group,GroupMember,GroupTitle

# Create your views here.

# Render the User Dashboard Home page:
@login_required
def profile_view(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    profile = Profile.objects.get(uuid=request.session["profile"])
    try:
        groups = GroupMember.objects.get(profile=request.session["profile"])
        primaryGroup = GroupMember.objects.get(profile=request.session["profile"],primary=True)
    except GroupMember.DoesNotExist:
        groups = []
        primaryGroup = False

    widgets = dynapages.PageWidget.objects.order_by('order').filter(page=profile.dynapage)
    context = {'community':community,'vhost':vhost,'profile':profile,'widgets':widgets,'groups':groups,'primaryGroup':primaryGroup,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,profile.dynapage.template.filename,context)

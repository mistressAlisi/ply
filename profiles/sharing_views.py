from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts
from profiles.models import Profile
from metrics.models import ProfilePageHit
from metrics.toolkit import request_data_capture

# Render the gallery Share card/page:
def profile(request,profile_id):
    # Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    else:
        request.session["community"] = str(community.uuid)
        profile = get_object_or_404(Profile,profile_id=profile_id)
        # Create the gallery metrics:
        profile_hit = ProfilePageHit.objects.create(type="SHAREOPEN",community=community,profile=profile)
        request_data_capture(request,profile_hit)
        profile_hit.save()
        return redirect('/profiles/@'+profile_id)

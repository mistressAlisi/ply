from django.http import Http404

# PLY
from ply.toolkit import vhosts

# Basic functions to support PLY requests:

# Find a community associated to the current request's URL and VHost, or redirect to "no Vhost found": Returns Community Object.
def vhost_community_or_404(request):
    try:
        vhost = request.META["HTTP_HOST"].split(":")[0];
        community = vhosts.get_vhost_community(hostname=vhost)
        return community
    except Exception as e:
        print(e)
        raise Http404("Community not Found!")

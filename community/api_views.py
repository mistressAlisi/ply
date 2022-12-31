from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
import json


import ply
from ply.toolkit import vhosts,profiles
from community.models import Friend





@login_required
def remove_friend(request,rmf):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    try:
        fobj = Friend.objects.get(pk=rmf)
    except Friend.NotFound:
        return JsonResponse({'res':"err",'e':'Relationship not found.'},safe=False)
    if ((fobj.friend1 != profile) & (fobj.friend2 != profile)):
        return JsonResponse({'res':"err",'e':'Relationship Access Denied.'},safe=False)
    fobj.delete()
    return JsonResponse({"res":"ok"},safe=False)

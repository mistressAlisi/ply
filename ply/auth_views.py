from django.shortcuts import render
from ply.toolkit import vhosts
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login as django_login
import ply

# Create your views here.

# Render the User Dashboard Home page:



#TODO: Encryption.
def login(request):
    vhost = request.META["HTTP_HOST"];
    community = (vhosts.get_vhost_community(hostname=vhost))
    username = request.POST['plyuserid']
    password = request.POST['plypass']
    user = authenticate(request, username=username, password=password)
    # User is found!!!
    if user is not None:
        django_login(request, user)
        # Setup the session:
        
        return JsonResponse({"res":{"login":"ok","community":"ok"}})
    else:
        # User not found!!!
        return JsonResponse({"res":{"login":"err"}})



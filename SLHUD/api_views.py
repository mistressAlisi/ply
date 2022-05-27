from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from PIL import Image
import secrets
import datetime

# PLY:
from SLHUD.models import SLParcelAgent,SLParcel

rand_source = secrets.SystemRandom()



# Update the Ply server with the known Agents in a Parcel:
def update_agents(request,parcel):
    if ('agl' in request.GET):
        agents = request.GET["agl"].split(",")
        ply_parcel = SLParcel.objects.get(uuid=parcel)
        count = 0
        for agent in agents:
            if agent != "":
                count +=1
                ao = SLParcelAgent.objects.get_or_create(parcel=ply_parcel,uuid=agent)[0]
                ao.last_seen = datetime.datetime.now(datetime.timezone.utc)
                ao.online = True
                ao.save()
        print(f"Found and tracked {count} agents.")
        return JsonResponse({"res":"ok"},safe=False)

    else:
        return JsonResponse({"res":"err","type":"No Agent List."},safe=False)

#
def action_roll(request):
    sides = request.POST["sides"]
    count = request.POST["count"]
    message = request.POST["message"]
    current = 0
    while (current < count):

        current += 1
    return JsonResponse({"res":"ok"},safe=False)

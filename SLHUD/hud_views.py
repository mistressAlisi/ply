#DJANGO:
from django.shortcuts import render
#PLY:
from ply import toolkit
from SLHUD.models import SLAgent,SLParcel

def start(request,parcel,agent):
    community = toolkit.reqtools.vhost_community_or_404(request)
    request.session["sl_agent"] = str(agent)
    request.session["sl_parcel"] = str(parcel)
    ply_agent = SLAgent.objects.filter(uuid=agent)[0]
    ply_agent.remote_addr = request.META["REMOTE_ADDR"]
    ply_agent.save()
    request.session["profile"] = str(ply_agent.profile.uuid)
    ply_parcel = SLParcel.objects.get(uuid=parcel)
    context = {'agent':agent,'parcel':parcel,'community':community,'ply_agent':ply_agent,'ply_parcel':ply_parcel}
    return render(request,'SLHUD/start.html',context)


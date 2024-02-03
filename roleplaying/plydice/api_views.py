from django.contrib.auth.decorators import login_required
from ply.toolkit import logger as plylog
from django.http import JsonResponse
from django.db import transaction
from communities.profiles.models import Profile
from ply.toolkit import streams as stream_toolkit
import secrets
from roleplaying.plydice.models import DiceRoll,DiceEvent,DiceEventRoll
from communities.community.models import Community
log = plylog.getLogger('plydice.api_views',name='plydice.api_views')
#queue = GalleryPublisher(ply.settings.PLY_MSG_BROKER_URL,log)
#queue.start()


@login_required
@transaction.atomic
def generic_roll(request,count,sides):
    ur = secrets.SystemRandom()
    rolltype='GENERIC'
    profile = Profile.objects.get(uuid=request.session['profile'])
    comm = Community.objects.get(uuid=request.session["community"])
    results = []
    if 'reason' in request.GET:
        reason = request.GET['reason']
    else:
        reason = 'Generic Roll'
    if 'th' in request.GET:
        th = int(request.GET['th'])
    else:
        th = int((count*sides)/2)
    if (count < 1):
        return JsonResponse("Need at least one dice!",safe=False)
    if (sides < 2):
        return JsonResponse("Need at least two sides!",safe=False)
    tcount = 0
    total = 0;
    while (tcount < count):
        droll = ur.randrange(1,sides)
        results.append(droll)
        total += droll
        tcount +=1
    rawdata = {'type':rolltype,'reason':reason,'dice':results}
    diceRoll = DiceRoll(profile=profile,community=comm,type=rolltype,threshold=th,count=count,sides=sides,result=total,contents_json=rawdata)
    diceRoll.save()
    diceEvent = DiceEvent(community=comm,profile=profile,type=rolltype)
    diceEvent.save()
    diceEventR = DiceEventRoll(community=comm,event=diceEvent,roll=diceRoll)
    diceEventR.save()

    # Now add to stream(s):
    duuid = str(diceEvent.uuid);
    rawdata['event'] = duuid
    stream_toolkit.post_to_active_profile(request,"application/ply.stream.diceroll",duuid,rawdata)
    stream_toolkit.post_to_active_profile(request,"application/ply.stream.diceroll",duuid,rawdata,"PLYDICE")
    if total >= th:
        res = 'SUCCESS'
    else:
        res = 'FAIL'
    result = {'type':rolltype,'reason':reason,'diecount':count,'diesides':sides,'total_roll':total,'dice':results,'event':diceEvent.uuid,'threshold':th,'result':res}
    return JsonResponse(result,safe=False)


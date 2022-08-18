from django.shortcuts import render
from django.core import serializers
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,file_uploader,logger as plylog,reqtools
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q
from profiles.models import Profile
from community.models import Community
from ply.toolkit.reqtools import vhost_community_or_404
from ply.toolkit import streams as stream_toolkit,file_uploader,profiles as toolkit_profiles
import json
import ply
import importlib
import os
import secrets
from django.utils.text import slugify
from plydice.models import DiceRoll,DiceEvent,DiceEventRoll
from django.contrib.auth.hashers import check_password
from community.models import Community
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
    if total >= th:
        res = 'SUCCESS'
    else:
        res = 'FAIL'
    result = {'type':rolltype,'reason':reason,'diecount':count,'diesides':sides,'total_roll':total,'dice':results,'event':diceEvent.uuid,'threshold':th,'result':res}
    return JsonResponse(result,safe=False)


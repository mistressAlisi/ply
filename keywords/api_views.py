from django.shortcuts import render
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,file_uploader,logger as plylog
from gallery.uploader import upload_plugins_builder
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q
from keywords.models import Keyword
from profiles.models import Profile
import json
import ply

log = plylog.getLogger('keywords.api_views',name='keywords.api_views')
@login_required
def get_keywords(request,search_str):
    keywords = Keyword.objects.filter(active=True,hidden=False,archived=False).filter(Q(keyword__icontains=search_str)|Q(hash__icontains=search_str))
    kw = []
    for k in keywords:
        kw.append({"n":k.keyword,"i":k.items,"l":k.likes,"d":k.dislikes,"c":k.comments,"s":k.shares,'h':k.hash})
    return JsonResponse(kw,safe=False)


def get_keywords_all(request):
    keywords = Keyword.objects.filter(active=True,hidden=False,archived=False)
    kw =[]
    for k in keywords:
        kw.append({"n":k.keyword,"i":k.items,"l":k.likes,"d":k.dislikes,"c":k.comments,"s":k.shares,'h':k.hash})
    return JsonResponse(kw,safe=False)

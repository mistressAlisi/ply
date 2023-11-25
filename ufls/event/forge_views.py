import datetime,uuid,json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from ufls.event.models import Event,EventCommunityMapping
from django.conf import settings
from ply.toolkit import vhosts,contexts
from ply.toolkit import logger as plylog
from .forms import EventForm
from ufls.event.models import Event
from communities.community.models import Community
log = plylog.getLogger('ufls.event.forge_views',name='ufls.event.forge_views')


@login_required
def create_event(request):
    vhost,community,context = contexts.default_context(request)
    event_form = EventForm()
    context["event_form"] = event_form
    return render(request,"ufls.event/create.html",context)

def link_community(request):
    vhost,community,context = contexts.default_context(request)
    com = Community.objects.filter(system=False)
    context.update({'communities':com})
    return render(request,"ufls.event/link.html",context)

@login_required
def event_table(request):
    vhost,community,context = contexts.default_context(request)
    events = Event.objects.all()
    context.update({'events':events})
    return render(request,"ufls.event/table.html",context)

@login_required
def event_query(request):
    vhost,community,context = contexts.default_context(request)
    events = Event.objects.all()
    context.update({'events':events})
    return render(request,"ufls.event/query.html",context)

@login_required
def event_modify(request):
    vhost,community,context = contexts.default_context(request)
    events = Event.objects.all()
    context.update({'events':events})
    return render(request,"ufls.event/modify.html",context)
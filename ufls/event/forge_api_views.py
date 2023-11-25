import datetime,uuid,json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

from communities.community.models import Community
from ufls.event.models import Event,EventCommunityMapping
from django.conf import settings
from ply.toolkit import vhosts,contexts
from ply.toolkit import logger as plylog
from .forms import EventForm,EventCommunityMappingForm
log = plylog.getLogger('ufls.event.forge_api_views',name='ufls.event.forge_api_views')
@login_required
def create_event_handle(request):
    event_form = EventForm(request.POST)
    # New event:
    if event_form.data["uuid"] == "":
        if not event_form.is_valid():
            return JsonResponse({"res":"err","e":event_form.errors}, safe=False)
        else:
            event_form.save()
            return JsonResponse({"res":"ok","pk":event_form.instance.pk},safe=False)
    # Existing Event:
    else:
        ev = get_object_or_404(Event, pk=event_form.data["uuid"])
        event_form = EventForm(request.POST,instance=ev)
        if not event_form.is_valid():
            return JsonResponse({"res": "err", "e": event_form.errors}, safe=False)
        else:
            event_form.save()
            return JsonResponse({"res": "ok", "pk": event_form.instance.pk}, safe=False)



@login_required
def query_handle(request,event):
    vhost,community,context = contexts.default_context(request)
    ev = get_object_or_404(Event,pk=event)
    ecm = EventCommunityMapping.objects.filter(event=ev)
    context.update({'event':ev,'ecm':ecm})
    return render(request,"ufls.event/query_render.html",context)


@login_required
def link_handle(request,com):
    vhost,community,context = contexts.default_context(request)
    com = get_object_or_404(Community,pk=com)
    ecm = EventCommunityMapping.objects.filter(community=com)
    if (len(ecm) > 0):
        form = EventCommunityMappingForm(instance=ecm[0])
    else:
        form = EventCommunityMappingForm(initial={'community': com,'uuid':None})
    context.update({'com':com,'form':form})
    return render(request,"ufls.event/link_render.html",context)

@login_required
def link_create_handle(request):
    vhost,community,context = contexts.default_context(request)
    form = EventCommunityMappingForm(request.POST)
    if form.data["uuid"] != "":
        ecm = EventCommunityMapping.objects.get(uuid=form.data["uuid"])
        form = EventCommunityMappingForm(request.POST, instance=ecm)
        if form.is_valid():
            form.save()
            return JsonResponse({"res": "ok", "pk": form.instance.pk}, safe=False)
        else:
            return JsonResponse({"res": "err", "e": form.errors}, safe=False)

    else:
        com = Community.objects.get(pk=form.data["community"])
        ev = Event.objects.get(pk=form.data["event"])
        ecm = EventCommunityMapping.objects.get_or_create(community=com)[0]
        ecm.event=ev
        if form.data['active'] == "On":
            ecm.active=True
        else:
            ecm.active=False
        ecm.save()
        return JsonResponse({"res": "ok", "pk": ecm.pk}, safe=False)

@login_required
def edit_event_handle(request,event):
    vhost,community,context = contexts.default_context(request)
    ev = get_object_or_404(Event,pk=event)
    event_form = EventForm(instance=ev)
    context["event_form"] = event_form
    return render(request,"ufls.event/edit.html",context)
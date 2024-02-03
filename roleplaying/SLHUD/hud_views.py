#DJANGO:
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
#PLY:
import ply
from ply import toolkit
from roleplaying.SLHUD.models import SLAgent,SLParcel,SLHUDSettings

def start(request,parcel,agent):
    community = toolkit.reqtools.vhost_community_or_404(request)
    request.session["sl_agent"] = str(agent)
    request.session["sl_parcel"] = str(parcel)
    try:
        ply_parcel = SLParcel.objects.get(uuid=parcel)
        try:
            ply_agent = SLAgent.objects.get(uuid=agent)
            ply_agent.remote_addr = request.META["REMOTE_ADDR"]
            ply_agent.save()
            request.session["profile"] = str(ply_agent.profile.uuid)
            return redirect("/SLHUD/");
        except SLAgent.DoesNotExist:
            settings = SLHUDSettings.objects.get(community=community)
            context = {'agent':agent,'parcel':parcel,'community':community,'ply_parcel':ply_parcel,'settings':settings}
            return render(request,'SLHUD/registration/start.html',context)
    except SLParcel.DoesNotExist:
            return render(request,'SLHUD/errors/no-SLparcel.html',{})


def login(request,parcel,agent):
    community = toolkit.reqtools.vhost_community_or_404(request)
    request.session["sl_agent"] = str(agent)
    request.session["sl_parcel"] = str(parcel)
    if 'plypass' in request.POST:
        user = authenticate(request, username=request.POST['plyuserid'], password=request.POST['plypass'])
        if user is not None:
            request.session['sl_usermap'] = str(user.pk)
            return redirect("/SLHUD/select/profile");
        else:
            err = "User and Password combination not found."
            ply_parcel = SLParcel.objects.get(uuid=parcel)
            settings = SLHUDSettings.objects.get(community=ply_parcel.community)
            context = {'agent':agent,'parcel':parcel,'community':community,'ply_parcel':ply_parcel,'settings':settings,'errstr':err}
            return render(request,'SLHUD/login/login.html',context)

    try:
        ply_parcel = SLParcel.objects.get(uuid=parcel)
        try:
            settings = SLHUDSettings.objects.get(community=ply_parcel.community)
            context = {'agent':agent,'parcel':parcel,'community':community,'ply_parcel':ply_parcel,'settings':settings}
            return render(request,'SLHUD/login/login.html',context)
        except SLAgent.DoesNotExist:
            settings = SLHUDSettings.objects.get(community=ply_parcel.community)
            context = {'agent':agent,'parcel':parcel,'community':community,'ply_parcel':ply_parcel,'settings':settings}
            return render(request,'SLHUD/errors/no-SLparcel.html',{})
    except SLParcel.DoesNotExist:
            return render(request,'SLHUD/errors/no-SLparcel.html',{})



def select_profile(request):
        community = toolkit.reqtools.vhost_community_or_404(request)
        agent = request.session["sl_agent"]
        parcel = request.session["sl_parcel"]
        ply_parcel = SLParcel.objects.get(uuid=parcel)
        all_profiles = toolkit.profiles.get_all_available_profiles(request.session['sl_usermap'],community)
        settings = SLHUDSettings.objects.get(community=ply_parcel.community)
        context = {'settings':settings,'agent':agent,'parcel':parcel,'community':community,'profiles':all_profiles,'av_path':ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,'SLHUD/select/profile.html',context)


def select_profile_activate(request,profile):
        community = toolkit.reqtools.vhost_community_or_404(request)
        agent = request.session["sl_agent"]
        parcel = request.session["sl_parcel"]
        user = User.objects.get(pk=request.session['sl_usermap'])
        profile = ply.toolkit.profiles.get_profile_for_user(user,profile)
        slagent = SLAgent.objects.get(uuid=agent)
        if ((profile is False) or (slagent.owner != user)):
            #Access Violation!
            return render(request,'SLHUD/errors/access-denied.html',{})
        slagent.profile = profile
        slagent.save()
        request.session["profile"] = str(profile.uuid)
        return redirect("/SLHUD/");



def hud_index(request):
        community = toolkit.reqtools.vhost_community_or_404(request)
        _agent = request.session["sl_agent"]
        _parcel = request.session["sl_parcel"]
        parcel = SLParcel.objects.get(uuid=_parcel)
        agent = SLAgent.objects.get(uuid=_agent)
        settings = SLHUDSettings.objects.get(community=parcel.community)
        context = {'settings':settings,'agent':agent,'parcel':parcel.uuid,'community':community,'av_path':ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
        return render(request,'SLHUD/start.html',context)

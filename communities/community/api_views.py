from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
import json


import ply
from ply.toolkit import vhosts,profiles,community as community_toolkit
from communities.community.models import Friend,Follower
from communities.profiles.models import Profile




@login_required
def add_friend(request,target):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    try:
        tprofile = Profile.objects.get(uuid=target);
        if not community_toolkit.are_friends(profile,tprofile,community):
            community_toolkit.add_friend(profile,tprofile,community)
        else:
            return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)
        return JsonResponse({'res':"ok"},safe=False)
    except Exception as e:
        print("Unable to frtiend:")
        print(e);
        return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)


@login_required
def un_friend(request,target):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    try:
        tprofile = Profile.objects.get(uuid=target);
        if community_toolkit.are_friends(profile,tprofile,community):
            community_toolkit.un_friend(profile,tprofile,community)
        else:
            return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)
        return JsonResponse({'res':"ok"},safe=False)
    except Exception as e:
        print("Unable to frtiend:")
        print(e);
        return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)




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



@login_required
def follow_profile(request,target):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))

    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    try:
        tprofile = Profile.objects.get(uuid=target);
        if not community_toolkit.is_following_profile(profile,tprofile,community):
            community_toolkit.follow_profile(profile,tprofile,community)
        else:
            return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)
        return JsonResponse({'res':"ok"},safe=False)
    except Exception as e:
        print("Unable to follow:")
        print(e);
        return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)

@login_required
def unfollow_profile(request,target):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))

    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    try:
        tprofile = Profile.objects.get(uuid=target);
        if community_toolkit.is_following_profile(profile,tprofile,community):
            community_toolkit.unfollow_profile(profile,tprofile,community)
        else:
            return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)
        return JsonResponse({'res':"ok"},safe=False)
    except Exception as e:
        print("Unable to unfollow:")
        print(e);
        return JsonResponse({'res':"err",'e':'Integrity Error.'},safe=False)

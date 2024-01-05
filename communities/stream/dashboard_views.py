from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import vhosts,profiles
from communities.profiles.models import Profile
import ply
import uuid
from communities.stream.forms import CreateStreamForm
from communities.stream.models import Stream, StreamMessage, StreamProfileXMPPSettings, StreamXMPPSettings
from media.gallery.core import serialisers
from ply.toolkit.contexts import default_context
from ply.toolkit.crypto import random_password


# Create your views here.

# Render the User Dashboard Home page:
@login_required
def profile_stream(request):
    """
    @brief ...
    :param request: p_request:...
    :type request: t_request:str
    :param profile_id: p_profile_id:...
    :type profile_id: t_profile_id:<callable>
    :returns: ${r:...}
    """

    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = profiles.get_active_profile(request)
    request.session["community"] = str(community.uuid)
    stream = Stream.objects.get_or_create(community=community,profile=profile,root_stream=True,type="PROFILE")[0]
    stream.views = stream.views+1
    stream.save()
    messages = StreamMessage.objects.filter(stream=stream).order_by('created')
    # Create the core metrics:
    #gal_hit = GalleryProfilePageHit.objects.create(profile=stream_profile,type="GALPAGE",community=community)
    #request_data_capture(request,gal_hit)
    # Now render the page:
    #colls = serialisers.serialise_community_per_profile_items(request,stream_profile)
    context = {'community':community,'vhost':vhost,'profile':profile,'current_profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,"stream":stream,"messages":messages}
    return render(request,'stream/dashboard/profile_stream.html',context)


@login_required
def view_stream(request):
    colls = serialisers.serialise_profile_collection_items(request)
    profile = Profile.objects.get(uuid=request.session["profile"])
    stream = Stream.objects.get(uuid=uuid.UUID('309daa0f-7618-4071-b3ab-0665969ea1ff'))
    messages = StreamMessage.objects.filter(stream=stream)
    context = {"colls":colls,"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'stream':stream,'messages':messages}
    return render(request,"stream/dashboard/dashboard.html",context)
    #return JsonResponse(colls,safe=False)   


@login_required
def create_stream(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    profile = Profile.objects.get(uuid=request.session["profile"])
    streamForm = CreateStreamForm(community=community,profile=profile)
    context = {"base_url":ply.settings.PLY_GALLERY_FILE_URL_BASE_URL,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,"streamForm":streamForm}
    return render(request,'stream/dashboard/create_stream.html',context)
    #return JsonResponse(colls,safe=False)

@login_required
def configure_xmpp(request):
    context,vhost,community,profile = default_context(request)
    context["app_password"] = random_password(24)
    site_settings = StreamXMPPSettings.objects.get_or_create()[0]
    try:
        settings = StreamProfileXMPPSettings.objects.get(profile=profile)
    except:
        # Is registration enabled?
        if not site_settings.enabled or not site_settings.self_reg:
            return render(request, 'stream/dashboard/xmpp/disabled.html', context)
        else:
            context["site_settings"] = site_settings

            return render(request, 'stream/dashboard/xmpp/setup/index.html', context)
    context["site_settings"] = site_settings
    context["xmpp_settings"] = settings
    return render(request,'stream/dashboard/xmpp/configure.html',context)
    #return JsonResponse(colls,safe=False)

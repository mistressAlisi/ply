from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.
# PLY
import ply
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from gallery import serialisers
from gallery.models import GalleryCollection,GalleryItemsByCollectionPermission
from metrics.models import GalleryCollectionPageHit,GalleryProfilePageHit,GalleryHomePageHit
from metrics.toolkit import request_data_capture
from stream.forms import StreamSettingsForm
from stream.models import Stream,StreamMessage,MessagesPerStreamView,StreamMessageKeywords
from group.models import Group


def view_message(request,muuid):
    """
    @brief Render the specified message with a specific uuid
    :param request: p_request:Django request
    :param muuid: p_muuid:The UUID of the message to retrieve.
    :type muuid: t_muuid:UUID
    :returns: r:Rendered Stream Message as Django View
    """
    message = get_object_or_404(StreamMessage,uuid=muuid)
    if (message.type == "application/ply.stream.gallery"):
        """
        Get collection / Item data (get a thumbnail), this is a gallery card:
        """
        item = GalleryItemsByCollectionPermission.objects.filter(gc_uuid=message.contents_json["col"],gci_uuid=message.contents_json["item"],gif_thumbnail=True).order_by('-gif_size')[0]
    else:
        item = ""
    context = {"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'m':message,'i':item}
    return render (request,'stream_message_card.html',context)


# Render the Gallery page for a given profile:
def profile_steam(request,profile_id):
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
    sideBar = SideBarBuilder()
    stream_profile = get_object_or_404(Profile,profile_id=profile_id)
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
        if (profile == stream_profile):
            settingsForm = StreamSettingsForm()
        else:
            settingsForm = False
    else:
        profile = False
        all_profiles = False
        settingsForm = False
    request.session["community"] = str(community.uuid)
    stream = Stream.objects.get_or_create(community=community,profile=stream_profile,root_stream=True,type="PROFILE")[0]
    stream.views = stream.views+1
    stream.save()
    updated_keywords = []
    messages = StreamMessage.objects.filter(stream=stream).order_by('created')
    for msg in messages:
        kws = StreamMessageKeywords.objects.filter(message=msg)
        # only update keyword views ONCE per page rendering:
        for k in kws:
            if k.keyword.id not in updated_keywords:
                updated_keywords.append(k.keyword.id)
                k.keyword.views += 1
                k.keyword.save()
    # Create the gallery metrics:
    #gal_hit = GalleryProfilePageHit.objects.create(profile=stream_profile,type="GALPAGE",community=community)
    #request_data_capture(request,gal_hit)
    # Now render the page: 
    #colls = serialisers.serialise_community_per_profile_items(request,stream_profile)
    context = {'community':community,'vhost':vhost,'profile':stream_profile,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'url_path':request.path,'settings_form':settingsForm,"stream":stream,"messages":messages}
    return render(request,'stream_profile_index_view.html',context)


# Render the Gallery page for a given profile:
def community_stream(request):
    """
    @brief Render page for the community stream view (all the posts in the streams belognging to the community)
    :param request: p_request:Django Request
    :type request: t_request:mixed
    :returns: rDjango Render View
    """

    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
    else:
        profile = False
        all_profiles = False
        settingsForm = False
    request.session["community"] = str(community.uuid)
    updated_keywords = []
    messages = MessagesPerStreamView.objects.filter(community=community,stream_type="PROFILE").order_by('message_created')
    for msg in messages:
        kws = StreamMessageKeywords.objects.filter(message=msg.id)
        # only update keyword views ONCE per page rendering:
        for k in kws:
            if k.keyword.id not in updated_keywords:
                updated_keywords.append(k.keyword.id)
                k.keyword.views += 1
                k.keyword.save()
    # Create the gallery metrics:
    #gal_hit = GalleryProfilePageHit.objects.create(profile=stream_profile,type="GALPAGE",community=community)
    #request_data_capture(request,gal_hit)
    # Now render the page:
    #colls = serialisers.serialise_community_per_profile_items(request,stream_profile)
    # NOTE: profile added to context to support widget rendering :)
    context = {'community':community,'vhost':vhost,'current_profile':profile,"profiles":all_profiles,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,"messages":messages,'profile':profile}
    return render(request,'stream_community_index_view.html',context)


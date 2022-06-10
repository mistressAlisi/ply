from django.http import Http404

# PLY
#from ply.toolkit import vhosts
from stream.models import Stream,StreamMessage
from community.models import Community
from profiles.models import Profile
# Basic functions to support PLY requests:


def post_to_active_profile(request,content_type,contents_text,contents_json):
    """
    @brief Post a message to the active ROOT STREAM profile of the profile and community in request session space.
    :param request: p_request:Django Request
    :type request: t_request:mixed
    :param content_type: p_content_type:Content Type, default: "text/plain"
    :type content_type: t_content_type:mixed
    :param contents_text: p_contents_text:Text Contents
    :type contents_text: t_contents_text:mixed
    :param contents_json: p_contents_json:JSON Contents
    :type contents_json: t_contents_json:mixed
    :returns: r:Message UUID
    """
    community = Community.objects.get(uuid=request.session['community'])
    profile = Profile.objects.get(uuid=request.session['profile'])
    stream = Stream.objects.get(community=community,profile=profile,root_stream=True,type="PROFILE")
    stream.nodes += 1
    stream.save()
    message = StreamMessage(stream=stream,author=profile,type=content_type,contents_text=contents_text,contents_json=contents_json)
    message.save()
    return message.uuid

def post_to_profile_stream(profile,community,content_type,contents_text,contents_json):
    """
    @brief Post a message to the specified profile's ROOT STREAM in the specified community.
    :param profile: p_profile:Profile Object
    :type profile: p_profile:profile Object
    :param community: p_community:Community Object
    :type community: p_community:Community Object
    :param content_type: p_content_type:Content Type, default: "text/plain"
    :type content_type: t_content_type:mixed
    :param contents_text: p_contents_text:Text Contents
    :type contents_text: t_contents_text:mixed
    :param contents_json: p_contents_json:JSON Contents
    :type contents_json: t_contents_json:mixed
    :returns: r:Message UUID
    """
    community = Community.objects.get(uuid=request.session['community'])
    profile = Profile.objects.get(uuid=request.session['profile'])
    stream = Stream.objects.get(community=community,profile=profile,root_stream=True,type="PROFILE")
    stream.nodes += 1
    stream.save()
    message = StreamMessage(stream=stream,author=profile,type=content_type,contents_text=contents_text,contents_json=contents_json)
    message.save()
    return message.uuid

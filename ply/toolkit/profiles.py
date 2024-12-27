"""
toolkit/profiles.py
====================================
Toolkit utilities for interacting with Ply Profiles
"""
import uuid

from ply.toolkit.logger import getLogger
from communities.profiles.models import Profile
from communities.community.models import ProfilePerCoummunityView

# get_vhost_community: Find the right community node for the given Vhost.
# To match VHosts, we must at least match the host name, and optionally, the iapddr.
# 

logging = getLogger('toolkit.vhosts',name='toolkit.vhosts')
#print(vhost_logger)


def get_active_profile(request):
    """
    @brief Return the active profile object from the session attached to the request.
    ===============================
    :param request: p_request:Django Request Object
    :type request: t_request:str
    :returns: r:Profile object
    """
    if 'profile' not in request.session:
       try:
           profile = Profile.objects.get(creator=request.user,archived=False,blocked=False,system=False,placeholder=False)
       except:
           # If we are a super user, we are allowed to use the system profile - this is needed to allow profile-less community management and to complete setup:
           if request.user.is_superuser == True:
                profile = Profile.objects.get(creator=request.user,archived=False,blocked=False,system=True,placeholder=False)
           else:
               return None
       request.session['profile'] = str(profile.uuid)
       request.session.modified = True
    else:
       try:
           profile = Profile.objects.filter(uuid=request.session['profile'])[0]
       except profile.NotFound as e:
            return None
        
    request.session.placeholder = False
    return profile
    
# Returns all the profiles associated with the User:       
def get_all_profiles(request,system=False):
    """
    Return all the profiles in the community for the user in the request

    :param kind: request obj Django Request Object
    :type kind: list[str] or None
    :return: a Profiles QueryDict
    :rtype: Profiles object

   """
    try:
        profiles = Profile.objects.filter(creator=request.user,archived=False,blocked=False,system=system,placeholder=False)
    except TypeError:
        return []
    return profiles
    


# create_placeholder_profile create a new 'placeholder' profile that will be hopefully populated by the user. This is a "new" profile that would be used as the basis of a new character by the forge module, for example.
# NOTE: It's up to the forge, or whatever module is creating this profile to UNPLACEHOLDER it, and to create the dynaPage structure(s) needed for the profile to render correctly at all.
# WARNING: DON'T SCREW THE NOTE'd comment UP - it WILL break your installation!
def get_placeholder_profile(request):
       profile = Profile.objects.filter(creator=request.user,archived=False,blocked=False,placeholder=True).first()
       if profile is None:
           profile = Profile.objects.create(
               uuid=uuid.uuid4(),
               creator=request.user, archived=False, blocked=False, placeholder=True,
               profile_id=request.user.username.lower()
           )
       request.session['profile'] = str(profile.uuid)
       request.session.modified = True
       request.session.placeholder = True
       return profile

# Get a profile from the active, available ones assigned to the user:
def get_profile(request,puuid):
       profile = Profile.objects.get(pk=puuid,creator=request.user,archived=False,blocked=False,placeholder=False,system=False)
       request.session['profile'] = str(profile.uuid)
       return profile 

# Get all available profiles that match a given user id, and a given community:
def get_all_available_profiles(uid,community):
    profiles = ProfilePerCoummunityView.objects.filter(community=community,profile_creator=uid)
    return profiles


# Get a profile for the specified user, you must specify PUUID as well:
# If the passed user is not the owner of the passed profile uuid, False will be returned.
def get_profile_for_user(user,puuid):
    try:
       profile = Profile.objects.get(pk=puuid,creator=user,archived=False,blocked=False,placeholder=False,system=False)
       return profile
    except profile.objects.NotFound:
        return False


def get_default_profile():
    try:
       puuid = uuid.UUID('0011aa22-bb33-0001-0001-000000000001')
       profile = Profile.objects.get(pk=puuid,system=True)
       return profile
    except profile.objects.NotFound:
        return False

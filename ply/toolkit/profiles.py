"""
toolkit/profiles.py
====================================
Toolkit utilities for interacting with Ply Profiles
"""


from community.models import Community,VHost
from ply.toolkit.logger import getLogger
from profiles.models import Profile
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
       profile = Profile.objects.filter(creator=request.user,archived=False,blocked=False,system=False,placeholder=False)[0]
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
def get_all_profiles(request):
    """
    Return all the profiles in the community for the user in the request

    :param kind: request obj Django Request Object
    :type kind: list[str] or None
    :return: a Profiles QueryDict
    :rtype: Profiles object

   """
    profiles = Profile.objects.filter(creator=request.user,archived=False,blocked=False,system=False,placeholder=False)
    return profiles
    


# create_placeholder_profile create a new 'placeholder' profile that will be hopefully populated by the user. This is a "new" profile that would be used as the basis of a new character by the forge module, for example.
# NOTE: It's up to the forge, or whatever module is creating this profile to UNPLACEHOLDER it, and to create the dynaPage structure needed for the profile to render correctly at all.
def get_placeholder_profile(request):
       profile = Profile.objects.get_or_create(creator=request.user,archived=False,blocked=False,placeholder=True)[0]
       request.session['profile'] = str(profile.uuid)
       request.session.modified = True
       request.session.placeholder = True
       return profile

# Get a profile from the active, available ones assigned to the user:
def get_profile(request,puuid):
       profile = Profile.objects.get(pk=puuid,creator=request.user,archived=False,blocked=False,placeholder=False,system=False)
       request.session['profile'] = str(profile.uuid)
       return profile 

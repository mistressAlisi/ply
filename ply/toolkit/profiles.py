from community.models import Community,VHost
from ply.toolkit.logger import getLogger
from profiles.models import Profile
# get_vhost_community: Find the right community node for the given Vhost.
# To match VHosts, we must at least match the host name, and optionally, the iapddr.
# 

logging = getLogger('toolkit.vhosts',name='toolkit.vhosts')
#print(vhost_logger)

# get_active_profile will match the 'uuid' stored in request.session to the active profile from the database and return it. 
# if there is no profile set it will select the first available profile that is active, unblocked and unarchived that matches the user in request.user.

def get_active_profile(request):
   if 'profile' not in request.session:
       profile = Profile.objects.filter(creator=request.user,archived=False,blocked=False)[0]
       request.session['profile'] = str(profile.uuid)
       request.session.modified = True
   else:
       profile = Profile.objects.filter(uuid=request.session['profile'])[0]
   return profile
    
# Returns all the profiles associated with the User:        
def get_all_profiles(request):
    profiles = Profile.objects.filter(creator=request.user,archived=False,blocked=False)
    return profiles
    

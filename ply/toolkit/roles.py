from django.core.exceptions import PermissionDenied

from communities.community.models import CommunityAdmins, CommunityStaff
from ply import settings
from ply.toolkit import vhosts,levels,themes,profiles


def is_profile_admin(community,profile):
    """
    Check if a given profile is an admin for the specified community
    @param community:  Community Object
    @param profile:  Staff Object
    @return:  True or False
    """
    is_admin = CommunityAdmins.objects.filter(community=community, profile=profile, active=True)
    if (len(is_admin) < 1):
        return False
    return True


def is_profile_staff(community,profile):
    """
    Check if a given profile is Staff for the specified community
    @param community:  Community Object
    @param profile:  Staff Object
    @return:  True or False
    """
    is_staff = CommunityStaff.objects.filter(community=community, profile=profile, active=True)
    if (len(is_staff) < 1):
        return False
    return True


def get_profile_staff(community,profile):
    """
    Get a given profile's communityStaff object
    @param community:  Community Object
    @param profile:  Staff Object
    @return: CommuniyStaff Object.
    """
    try:
        is_staff = CommunityStaff.objects.get(community=community, profile=profile, active=True)
        return is_staff
    except:
        return False


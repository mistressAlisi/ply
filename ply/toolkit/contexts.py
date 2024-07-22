from django.core.exceptions import PermissionDenied

from communities.community.models import CommunityAdmins
from ply import settings
from ply.toolkit import vhosts, levels, themes, profiles, version
from ply.toolkit import roles

def default_context(request, current_profile=False):
    """
    Generate the basic Context required for any Ply view from any given Request.
    Supply a request object; returns 3 objects: vhost,community,context Dict, OR False if no community.
    @param request: Request object (ie, django request)
    @param current_profile: Current profile will be used to select the displayed profile. If none, default account profile will be specified.
    @return: Returns 4 objects: Context Dict, VHost object, Community object and Current Profile object.
    """
    vhost, community = vhosts.get_vhost_and_community(request)
    if community is None:
        raise NotImplementedError("No Virtual Host/Community found.")

    theme = themes.get_community_theme_or_def(community)
    ap = profiles.get_active_profile(request)
    if not current_profile:
        current_profile = ap
    all_profiles = profiles.get_all_profiles(request)
    vers = version.get_version_str

    context = {
        "community": community,
        "vhost": vhost,
        "THEME_PATH": theme.THEME_PATH,
        "av_path": settings.PLY_AVATAR_FILE_URL_BASE_URL,
        "ply_version": vers,
        "profile": ap,
        "current_profile": current_profile,
        "profiles": all_profiles,
    }

    return context, vhost, community, current_profile


def admin_context(request, current_profile=False):
    """
    As above; BUT will throw an exception if profile does not have admin rights for the community.
    @param request: Request object (ie, django request)
    @param current_profile: Current profile will be used to select the displayed profile. If none, default account profile will be specified.
    @return: Returns 4 objects: Context Dict, VHost object, Community object and Current Profile object.
    """
    a, b, c, d = default_context(request, current_profile)
    is_admin = roles.is_profile_admin(c, d)
    if not is_admin:
        raise PermissionDenied("You're not an admin! Shoo!")
    return a, b, c, d


def staff_context(request, current_profile=False):
    """
    As above; BUT will throw an exception if profile does not have staff rights for the community.
    @param request: Request object (ie, django request)
    @param current_profile: Current profile will be used to select the displayed profile. If none, default account profile will be specified.
    @return: Returns 4 objects: Context Dict, VHost object, Community object and Current Profile object.
    """
    a, b, c, d = default_context(request, current_profile)
    is_admin = roles.is_profile_staff(c, d)
    if not is_admin:
        raise PermissionDenied("You're not staff! Shoo!")
    return a, b, c, d

def admin_or_staff_context(request, current_profile=False):
    """
    As above; BUT will throw an exception if profile does not have staff rights for the community.
    @param request: Request object (ie, django request)
    @param current_profile: Current profile will be used to select the displayed profile. If none, default account profile will be specified.
    @return: Returns 4 objects: Context Dict, VHost object, Community object and Current Profile object.
    """
    a, b, c, d = default_context(request, current_profile)
    is_staff = roles.is_profile_staff(c, d)
    is_admin = roles.is_profile_admin(c, d)
    if not is_admin or is_staff:
        raise PermissionDenied("You're not an admin or staff! Shoo!")
    return a, b, c, d


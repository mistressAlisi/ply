from ply import settings
from ply.toolkit import vhosts,levels,themes,profiles
def default_context(request,current_profile=False):
    """
    Generate the basic Context required for any Ply view from any given Request.
    Supply a request object; returns 3 objects: vhost,community,context Dict, OR False if no community.
    """
    vhost,community = vhosts.get_vhost_and_community(request)
    if community is None:
        return False
    theme = themes.get_community_theme_or_def(community)
    ap = profiles.get_active_profile(request)
    if not current_profile:
        current_profile = ap
    all_profiles = profiles.get_all_profiles(request)
    context = {'community': community, 'vhost': vhost, 'THEME_PATH': theme.THEME_PATH,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'ply_version':settings.PLY_VERSION,'profile':ap,'current_profile':current_profile,'profiles':all_profiles}

    return vhost,community,context




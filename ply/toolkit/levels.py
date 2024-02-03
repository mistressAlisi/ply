"""
toolkit/profiles.py
====================================
Toolkit utilities for interacting with Ply Profile's Levels
"""
from ply.toolkit.logger import getLogger
from ply.toolkit import scripts,streams
from roleplaying.exp.models import ProfileExperience,ProfileExperienceHistory,LevelScript

logging = getLogger('toolkit.levels',name='toolkit.levels')

def can_levelup(profile,community):
    """
    @brief Return TRUE or FALSE whether the given profile CAN level up or not.
    ===============================
    :param profile: p_profile:Profile Object
    :type profile: p_profile:profile Object
    :param community: p_community:Community Object
    :type community: p_community:Community Object
    :returns: r:BOOLEAN
    """
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    logging.debug(f"Profile @{profile.profile_id}/{profile.uuid}: Can Level: {exo.can_level()}")
    return exo.can_level()


def levelup(profile,community):
    """
    @brief LEVELUP the given profile, if a new level is available ;)
    ===============================
    :param profile: p_profile:Profile Object
    :type profile: p_profile:profile Object
    :param community: p_community:Community Object
    :type community: p_community:Community Object
    :returns: r:BOOLEAN
    """
    exo = ProfileExperience.objects.get(community=community,profile=profile)
    nlvl = exo.next_level()
    if nlvl is False:
        return False
    if not exo.can_level(): return False
    logging.debug(f"Levelling up {profile.profile_id}...")
    exo.statpoints += nlvl.statpoints
    exo.skillpoints += nlvl.skillpoints
    exo.level = nlvl
    exo.save()
    logging.debug(f"Profile: @{profile.profile_id}/{profile.uuid}: Assigned Stat: {nlvl.statpoints} and Skill: {nlvl.skillpoints} points to profile from leveling up to {nlvl.level}...")
    # Now do the scripts:
    # Global scripts first:
    gscripts = LevelScript.objects.filter(community=community,level=nlvl)
    for scr in gscripts:
        logging.debug(f"Level Up: Executing Script {scr.script.function_name}...")
        scripts.exec_script(scr.script,community,profile)
    # Class Scripts next:
    gscripts = LevelScript.objects.filter(community=community,level=nlvl,classtype=exo.classtype)
    for scr in gscripts:
        logging.debug(f"Level Up: Executing Script {scr.script.function_name}...")
        scripts.exec_script(scr.script,community,profile)
    # And the audit history:
    peh = ProfileExperienceHistory(community=community,profile=profile,classtype=exo.classtype,expr=exo.expr,statpoints=exo.statpoints,skillpoints=exo.skillpoints,level=nlvl,reason=f"Level Up to {nlvl.level}")
    # Create the stream node(s):
    streams.post_to_profile_stream(profile,community,'ply.stream.levelup',f"Level Up to {nlvl.level}",{"level":nlvl.level,'uuid':str(nlvl.uuid)})
    # save and finish:
    peh.save()
    exo.save()
    return exo

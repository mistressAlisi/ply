"""
toolkit/profiles.py
====================================
Toolkit utilities for interacting with Ply Profile's Levels
"""
from community.models import Community,VHost
from ply.toolkit.logger import getLogger
from ply.toolkit import scripts,streams
from profiles.models import Profile
from stats.models import ClassType,ProfileStat,ProfileStatHistory
from exp.models import ProfileExperience,ProfileExperienceHistory,LevelScript
logging = getLogger('toolkit.stats',name='toolkit.stats')

def assign_stat(profile,community,stat,points=1):
    """
    @brief ASSIGN a given profile the given number of POINTS in the STAT specified (if allowed):
    ===============================
    :param profile: p_profile:Profile Object
    :type profile: p_profile:profile Object
    :param community: p_community:Community Object
    :type community: p_community:Community Object
    :param profilestat: p_stat:ProfileStat Object
    :type profilestat: p_stat:profileStat Object
    :param points: p_points:Integer
    :type points: p_integer:Number of Points to assign
    :returns: r:BOOLEAN FALSE if not allowed, -1 if illegal move, TRUE if stat assigned.
    """
    exp = ProfileExperience.objects.get(community=community,profile=profile)
    if ((points > exp.statpoints) or (points+stat.value > stat.stat.maximum)):
        logging.error(f"Profile: @{profile.profile_id}/{profile.uuid}: Cannot Assign Stat: {stat.stat.name} {points}!")
        return -1
    stat.value += points
    exp.statpoints -= points
    exp.save()

    stat.save()
    notes = f"Assigned {points} points to {stat.stat.name}"
    n_stat_h = ProfileStatHistory.objects.get_or_create(community=community,profile=profile,stat=stat.stat,value=stat.value,pminimum=stat.stat.minimum,pmaximum=stat.stat.maximum,notes=notes)[0]
    n_stat_h.save()
    logging.debug(f"Profile: @{profile.profile_id}/{profile.uuid}: Assigned Stat: {stat.stat.name} {points} points from exp pool. EXP pool stats at: {exp.statpoints}...")
    # Create the snapshost:
    exp.history_snapshot(notes)
    # Create the stream node(s):
    streams.post_to_profile_stream(profile,community,'ply.stream.statup',f"{points} Stat Point(s) Assigned to {stat.stat.name}",{"stat":str(stat.uuid),'points':points})
    return True


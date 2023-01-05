"""
toolkit/friends.py
====================================
Toolkit utilities for interacting with Friends:
"""
from community.models import Community,Friend,Follower


def are_friends(profile1,profile2,community):
    c_obj = Friend.objects.filter(friend1=profile1,friend2=profile2,community=community,approved_flag=True)|Friend.objects.filter(friend2=profile1,friend1=profile2,community=community,approved_flag=True)
    if (len(c_obj)) > 0:
        return True
    else:
        return False

def add_friend(profile_source,profile_dest,community):
     new_friend = Friend.objects.get_or_create(friend1=profile_source,friend2=profile_dest,community=community,)[0]
     new_friend.save()
     return True


def is_following_profile(profile_source,profile_dest,community):
    c_obj = Follower.objects.filter(source=profile_source,dest=profile_dest,community=community)
    if (len(c_obj)) > 0:
        return True
    else:
        return False


def follow_profile(profile_source,profile_dest,community):
     new_fol = Follower.objects.get_or_create(source=profile_source,dest=profile_dest,community=community)[0]
     new_fol.save()
     return True


def unfollow_profile(profile_source,profile_dest,community):
     new_fol = Follower.objects.filter(source=profile_source,dest=profile_dest,community=community)
     new_fol.delete()
     return True


def un_friend(profile1,profile2,community):
    c_obj = Friend.objects.filter(friend1=profile1,friend2=profile2,community=community,approved_flag=True)|Friend.objects.filter(friend2=profile1,friend1=profile2,community=community,approved_flag=True)
    if (len(c_obj)) > 0:
        c_obj.delete()
        return True
    else:
        return False

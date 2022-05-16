import uuid
from group.models import Group
from profiles.models import Profile
def get_placeholder():
    sp = Profile.objects.get(pk=uuid.UUID('0011aa22-bb33-0001-0001-000000000001'))
    return Group.objects.get_or_create(pk=uuid.UUID("76a21f77-aa11-0001-0001-000000000001"),creator=sp.creator,creator_profile=sp,system=True)[0]

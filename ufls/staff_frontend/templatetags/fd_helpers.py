import os

from django import template
from django.conf import settings
from django.db.models import Q

from registration.models import Badge
from staff.models import StaffAssignment

register = template.Library()

@register.simple_tag
def isBadgeDifferent(badgeRecord: Badge):
    return badgeRecord.number[0:1].isalpha()


@register.simple_tag
def filter_director_access(account):
    return StaffAssignment.objects.filter(
        Q(rank="Department Assistant Director")
        | Q(rank="Department Director")
        | Q(rank="Board Member"),
        user=account,
    )


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None

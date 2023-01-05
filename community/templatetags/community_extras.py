import datetime
from django import template
from ply.toolkit import community
register = template.Library()

@register.simple_tag(takes_context=True)
def is_friends_with(context,profile):
    return community.are_friends(profile,context["current_profile"],context["community"])

@register.simple_tag(takes_context=True)
def follows(context,profile):
    return community.is_following_profile(context["current_profile"],profile,context["community"])


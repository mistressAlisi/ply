from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import ply
from ply.toolkit import vhosts,profiles
from communities.community.models import Friend_ExpLvl_View
from communities.profiles.models import Profile


# Create your views here.

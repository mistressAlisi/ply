from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv

from django.db import IntegrityError

from communities.community.models import (
    Community,
    CommunitySidebarMenu, CommunityDashboardType
)
from communities.profiles.models import Profile
from ply.models import PlyApplication


class Command(BaseCommand):
    help = "Populates all the available Dashboard/Sidebar menus with registered Ply Applications. (Hint: Run register_plyapps first!). Use _all_ for all communities."

    def add_arguments(self, parser):
        parser.add_argument("community", type=str)

    def handle(self, *args, **options):
        community = options["community"]
        if community == "_all_":
            cob = Community.objects.all()
        else:
            cob = Community.objects.filter(hash=community)
        if len(cob) < 1:
            self.stdout.write(
                self.style.ERROR(
                    f"No community found. Run setup/step1.sh and setup/step2.sh first, or specify a valid community hash!"
                )
            )
            return False
        for dt in CommunityDashboardType.objects.all():
            for c in cob:
                dtos = PlyApplication.objects.all()
                for d in dtos:
                    try:
                        self.stdout.write(f"Application: {d}, Mode: {dt.type}....")
                        csmo = CommunitySidebarMenu.objects.get_or_create(community=c,application_mode=dt.type,module=d)
                    except IntegrityError:
                        pass
        self.stdout.write(self.style.SUCCESS("Success!"))

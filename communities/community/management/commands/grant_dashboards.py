from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv
from communities.community.models import (
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    Community,
)
from communities.profiles.models import Profile


class Command(BaseCommand):
    help = "Grant the specified Dashboard type (or _all_ for all) to a specified user in a given community."

    def add_arguments(self, parser):
        parser.add_argument("community", type=str)
        parser.add_argument("user", type=str)
        parser.add_argument("dashboard_type", type=str)

    def handle(self, *args, **options):
        user = options["user"]
        dashboard_type = options["dashboard_type"]
        community = options["community"]
        if community == "__auto-during-setup__":
            try:
                cob = Community.objects.all()[0]
            except Exception as e:
                print(e)
                self.stdout.write(self.style.ERROR(f"No community found. Run setup/step1.sh and setup/step2.sh first!"))
                return False

        else:
            try:
                cob = Community.objects.get(hash=community)
            except Exception as e:
                print(e)
                self.stdout.write(self.style.ERROR(f"NO SUCH Community: '{community}'!"))
                return False
        try:
            if user == "__auto-during-setup__":
                uob = User.objects.all()[0]
            else:
                uob = User.objects.get(username=user)
        except Exception as e:
            print(e)
            self.stdout.write(self.style.ERROR(f"NO SUCH User: '{user}'!"))
            return False

        self.stdout.write(self.style.MIGRATE_HEADING(f"Selected User: {user}."))
        if dashboard_type == "_all_":
            dashboards = CommunityDashboardType.objects.filter(privileged=True)
        else:
            dashboards = CommunityDashboardType.objects.filter(type=dashboard_type,privileged=True)
        profiles = Profile.objects.filter(creator=uob)
        for dbt in dashboards:
            self.stdout.write(
                self.style.MIGRATE_LABEL(
                    f'Adding Dashboard Type: "{dbt.type}" for all profiles that belong to: {uob.username} in community {cob.hash}...'
                )
            )
            for profile in profiles:
                cpdr = CommunityProfileDashboardRoles.objects.get_or_create(
                    community=cob,
                    profile=profile,
                    type=dbt,
                )[0]
                cpdr.active = True
                cpdr.save()
        self.stdout.write(self.style.SUCCESS("Success!"))

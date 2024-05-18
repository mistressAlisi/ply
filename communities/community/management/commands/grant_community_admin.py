from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv
from communities.community.models import (
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    Community,
    CommunityAdmins,
)
from communities.profiles.models import Profile


class Command(BaseCommand):
    help = "Grant the specified user's profiles in a given community admin status."

    def add_arguments(self, parser):
        parser.add_argument("community", type=str)
        parser.add_argument("user", type=str)
        parser.add_argument("profile", type=str)

    def handle(self, *args, **options):
        user = options["user"]
        community = options["community"]
        profile = options["profile"]
        if community == "__auto-during-setup__":
            try:
                cob = Community.objects.all()[0]
            except Exception as e:
                print(e)
                self.stdout.write(
                    self.style.ERROR(
                        f"No community found. Run setup/step1.sh and setup/step2.sh first!"
                    )
                )
                return False

        else:
            try:
                cob = Community.objects.get(hash=community)
            except Exception as e:
                print(e)
                self.stdout.write(
                    self.style.ERROR(f"NO SUCH Community: '{community}'!")
                )
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

        if profile == "_all_":
            profiles = Profile.objects.filter(creator=uob)
        else:
            try:
                profiles = Profile.objects.filter(creator=uob, profile_id=profile)
            except:
                self.stdout.write(self.style.ERROR(f"NO SUCH Profile: '{profile}'!"))
                return False
        for profile in profiles:
            self.stdout.write(
                self.style.MIGRATE_LABEL(
                    f'Adding Profile: {uob.username}.@{profile.profile_id} [{profile.uuid}] as admin to: {cob.hash}'
                )
            )
            caob = CommunityAdmins.objects.get_or_create(
                community=cob, profile=profile
            )[0]
            caob.active = True
            caob.save()
        self.stdout.write(self.style.SUCCESS("All Done!"))

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv
from communities.community.models import (
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    Community,
    CommunityRegistry,
)
from core.dynapages.models import Page, Templates
from communities.profiles.models import Profile
from ply.toolkit import profiles


class Command(BaseCommand):
    help = "Creates the default Dynapage landing nodes for the specified dashboard mode(s) in the community if they don't exist. Use _all_ for all apps."

    def add_arguments(self, parser):
        parser.add_argument("community", type=str)
        parser.add_argument("dashboard_type", type=str)

    def handle(self, *args, **options):
        dashboard_type = options["dashboard_type"]
        community = options["community"]
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

        if dashboard_type == "_all_":
            dashboards = CommunityDashboardType.objects.filter(privileged=True)
        else:
            dashboards = CommunityDashboardType.objects.filter(
                type=dashboard_type, privileged=True
            )
        template = Templates.objects.get(
            template_id="dynapage-template-default-pdashboard-2C"
        )
        for dbt in dashboards:
            registry_key_str = f"__dashboard-landingPage-{dbt.type}"
            registry_key, created = CommunityRegistry.objects.update_or_create(
                key=registry_key_str, community=cob
            )
            if created:
                registry_key.name = registry_key_str
                registry_key.grouping_key = "community_appmode_dashboards"
                self.stdout.write(
                    self.style.MIGRATE_LABEL(
                        f'Creating Dynapage for Dashboard Type: "{dbt.type}" in community {cob.hash}...'
                    )
                )
                registry_key_str += f"-{cob.hash}"
                default_db_str = f"Default Dashboard for {dbt.descr}"
                page, page_created = Page.objects.get_or_create(slug=registry_key_str,template = template)
                page.label = default_db_str
                page.system = True
                page.widget_mode = dbt.type
                page.save()
                registry_key.uuid_value = page.pk
                registry_key.foreign_key_ref = "core.dynapages.page"
                registry_key.save()

        self.stdout.write(self.style.SUCCESS("Success!"))

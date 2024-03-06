from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv
from communities.community.models import (
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    Community,
)
from communities.community.models import Community


class Command(BaseCommand):
    help = "List all Communities."



    def handle(self, *args, **options):
        cobs = Community.objects.all()
        for cob in cobs:
            self.stdout.write(self.style.MIGRATE_LABEL(f"Community: [{cob.uuid}] Name: '{cob.name}' - hash: '{cob.hash}' Created: {cob.created}"))


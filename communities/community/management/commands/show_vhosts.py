from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os, csv
from communities.community.models import (
    CommunityDashboardType,
    CommunityProfileDashboardRoles,
    Community,
    VHost,
)
from communities.community.models import Community


class Command(BaseCommand):
    help = "List all VHosts."

    def handle(self, *args, **options):
        vhosts = VHost.objects.all()
        for vhst in vhosts:
            self.stdout.write(
                self.style.MIGRATE_LABEL(
                    f"VHost for Hostname: {vhst.hostname}, IP Addr: {vhst.ipaddr} - Community: {vhst.community.name}"
                )
            )

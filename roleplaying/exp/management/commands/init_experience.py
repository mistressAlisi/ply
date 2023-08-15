from django.core.management.base import BaseCommand

from bs4 import BeautifulSoup
from ply import system_uuids,settings
import os

from communities.community.models import Community
from roleplaying.exp.models import Level

class Command(BaseCommand):
    help = 'Creates the Base level: Level 1 in all communities: THIS SHOULD ONLY BE DONE ONCE PER SETUP!'


    def handle(self, *args, **options):
        # All profiles must be owned by the primary admin:
        comms = Community.objects.filter(archived=False,frozen=False)
        for community in comms:
        # Create the magic Profile in the System:
            self.stdout.write(self.style.SUCCESS(f"Creating Level 0 in Community: '{community.name}'...."))
            clevel = Level.objects.get_or_create(community=community,level=0,expr=-1)[0]
            clevel.save()
            self.stdout.write(self.style.SUCCESS(f"Creating Level 1 in Community: '{community.name}'...."))
            clevel = Level.objects.get_or_create(community=community,level=1,expr=0)[0]
            clevel.save()
        self.stdout.write(self.style.SUCCESS('Success!'))


from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os

from core.dynapages.models import Templates,Page,Widget,PageWidget
from communities.community.models import Community
from roleplaying.stats.models import BaseStat,ClassType

class Command(BaseCommand):
    help = 'Creates the Base "Citizen" class, and the base classes listed below! do it once per setup only!'


    def handle(self, *args, **options):
        comms = Community.objects.filter(archived=False,frozen=False)
        for community in comms:
            self.stdout.write(self.style.SUCCESS(f"Creating Base Class Type 'Citizen' in Community: '{community.name}'...."))
            cstat = ClassType.objects.get_or_create(community=community,name='Citizen',descr="Everyone is a Citizen!",selectable=True)[0]
            cstat.save()
            for sta in ['HP','MP','STA','Stun','Defence','Intelligence','Charisma','Strength']:
                self.stdout.write(self.style.SUCCESS(f"Creating Base Stat '{sta}' in Community: '{community.name}'...."))
                cstat = BaseStat.objects.get_or_create(community=community,name=sta,minimum=0,maximum=10,starting=1)[0]
                cstat.save()
        self.stdout.write(self.style.SUCCESS('Success!'))



from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from bs4 import BeautifulSoup
import uuid
from ply import system_uuids
from django.conf import settings
from django.contrib.auth.models import User
import os
import ply

from communities.community.models import Community,CommunityRegistry


class Command(BaseCommand):
    help = 'RegEdit-Clear: Clear the given [key] in the registry for the given [community].'

    def add_arguments(self, parser):
        parser.add_argument('community', type=str)
        parser.add_argument('key', type=str)
        parser.add_argument('confirm', type=str)




    def handle(self, *args, **options):
        comm = Community.objects.get(uuid=uuid.UUID(options["community"]))
        if options["confirm"] != "yes":
            self.stdout.write(self.style.WARNING("To clear this key, pass the third argument as 'yes'"))
            return False
        self.stdout.write(self.style.MIGRATE_LABEL(f'Clear value in Registry  with key [{options["key"]}] in Community [{comm.uuid}][{comm.name}]'))
        regobj,created = CommunityRegistry.objects.get_or_create(community=comm,key=options["key"])
        regobj.clear_all(True)
        regobj.save()
        self.stdout.write(self.style.SUCCESS('Success!'))

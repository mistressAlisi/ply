from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os
import ply

from communities.community.models import Community,CommunityRegistry


class Command(BaseCommand):
    help = 'GetReg: Get the value of the given [key] in the registry for the given [community].'

    def add_arguments(self, parser):
        parser.add_argument('community', type=str)
        parser.add_argument('key', type=str)




    def handle(self, *args, **options):
        comm = Community.objects.get(uuid=uuid.UUID(options["community"]))
        self.stdout.write(self.style.MIGRATE_LABEL(f'Value in Registry for key [{options["key"]}] in Community [{comm.uuid}][{comm.name}]:'))
        regobj = CommunityRegistry.objects.get(community=comm,key=options["key"])
        self.stdout.write(f"Text_value:{regobj.text_value}")
        self.stdout.write(f"int_value:{regobj.int_value}")
        self.stdout.write(f"json_value:{regobj.json_value}")
        self.stdout.write(f"bin_value:{regobj.bin_value}")
        self.stdout.write(f"bool_value:{regobj.bool_value}")
        self.stdout.write(f"uuid_value:{regobj.uuid_value}")
        self.stdout.write(self.style.SUCCESS('Success!'))


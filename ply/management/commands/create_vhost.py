from django.core.management.base import BaseCommand, CommandError
import uuid
from ply import system_uuids
from django.conf import settings
from django.contrib.auth.models import User
import os
import ply
from django.utils.text import slugify
from communities.community.models import Community,VHost,CommunityAdmins
from communities.profiles.models import Profile
from core.dynapages.models import Page
class Command(BaseCommand):
    help = 'Creates a VHost for an existing community'


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('***Existing Communities ****:'))
        cobs = Community.objects.all()
        for cob in cobs:
            self.stdout.write(self.style.MIGRATE_LABEL(f"Community: [{cob.uuid}] Name: '{cob.name}' - hash: '{cob.hash}' Created: {cob.created}"))
        self.stdout.write(self.style.SUCCESS('***Existing VHosts ****:'))
        vhosts = VHost.objects.all()
        for vhst in vhosts:
            self.stdout.write(
                self.style.MIGRATE_LABEL(
                    f"VHost for Hostname: {vhst.hostname}, IP Addr: {vhst.ipaddr} - Community: {vhst.community.name}"
                )
            )
        name = input("Enter Community name/slug?: ")
        if (name is None):
                self.stdout.write(self.style.ERROR('Community slug/name is needed'))
                return False
        slug = slugify(name)
        self.stdout.write(self.style.SUCCESS(f"Selecting Community '{name}' (@{slug})...."))
        com = Community.objects.get(hash=slug)
        self.stdout.write(self.style.SUCCESS(f"Proceeding to VHost creation"))
        newvhost = "n"
        while (newvhost != ""):
            newvhost = str(input(f"Enter hostname for additional VHost or press enter to continue: "))
            if (newvhost != "") :
                self.stdout.write(self.style.SUCCESS(f"Creating VHost '{newvhost}' for @{slug}..."))
                vh = VHost(community=com, hostname=newvhost)
                vh.save()
        self.stdout.write(self.style.SUCCESS('Success!'))

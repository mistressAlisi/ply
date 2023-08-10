from django.core.management.base import BaseCommand, CommandError
import uuid
from ply import system_uuids,settings
import os
import ply
from django.utils.text import slugify
from communities.community import Community,VHost

class Command(BaseCommand):
    help = 'Creates a Community and attaches it to a VHost.'


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Create Community:'))
        name = input("Enter Community Name?: ")
        if (name is None):
                self.stdout.write(self.style.ERROR('Community name is needed'))
                return False
        dslug = slugify(name)
        slug = str(input(f"Enter Slugified Name? DO NOT INCLUDE SPACES (Enter for Default: '{dslug}'): "))
        if (len(slug) == 0):
            slug = dslug
        self.stdout.write(self.style.SUCCESS(f"Creating Community '{name}' (@{slug})...."))
        com = Community(name=name,hash=slug)
        com.save()
        self.stdout.write(self.style.SUCCESS(f"Creating Default VHost for '127.0.0.1' for @{slug}..."))
        vh = VHost(community=com,hostname='127.0.0.1')
        vh.save()
        self.stdout.write(self.style.SUCCESS(f"Creating Default VHost for 'localhost' for @{slug}..."))
        vh = VHost(community=com,hostname='localhost')
        vh.save()
        self.stdout.write(self.style.SUCCESS('Success!'))

from django.core.management.base import BaseCommand, CommandError
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os
import ply
from django.utils.text import slugify
from communities.community.models import Community,VHost,CommunityAdmins
from communities.profiles.models import Profile
from core.dynapages.models import Page
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
        page = Page.objects.get(page_id=system_uuids.install_complete_uuid)
        com.dynapage = page
        com.save()
        self.stdout.write(self.style.SUCCESS(f"Creating Default VHost for '127.0.0.1' for @{slug}..."))
        vh = VHost(community=com,hostname='127.0.0.1')
        vh.save()
        self.stdout.write(self.style.SUCCESS(f"Creating Default VHost for 'localhost' for @{slug}..."))
        vh = VHost(community=com,hostname='localhost')
        vh.save()
        newvhost = "n"
        while (newvhost != ""):
            newvhost = str(input(f"Enter hostname for additional VHost or press enter to continue: "))
            if (newvhost != "") :
                self.stdout.write(self.style.SUCCESS(f"Creating Default VHost for '{newvhost}' for @{slug}..."))
                vh = VHost(community=com, hostname=newvhost)
                vh.save()
        self.stdout.write(self.style.SUCCESS(f"Creating Initial Admin for @{slug}..."))
        owner = User.objects.get(is_superuser=True)
        mprofile = Profile.objects.get_or_create(uuid=system_uuids.profile_uuid, creator=owner)[0]
        nca = CommunityAdmins(community=com,profile=mprofile,active=True)
        nca.save()
        self.stdout.write(self.style.SUCCESS('Success!'))

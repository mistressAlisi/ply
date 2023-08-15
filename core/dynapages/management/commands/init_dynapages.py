from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os

from core.dynapages.models import Templates,Page,Widget,PageWidget
from communities.profiles.models import Profile


class Command(BaseCommand):
    help = 'Creates the empty magical \"system\" profile that will hold a blank DynaPage template that will be applied to all created profiles and groups. THIS SHOULD ONLY BE DONE ONCE PER SETUP!'


    def handle(self, *args, **options):
        # All profiles must be owned by the primary admin:
        owner = User.objects.get(is_superuser=True)
        
        # Create the magic Profile in the System:
        self.stdout.write(self.style.SUCCESS('Creating Magic profile...'))
        mprofile = Profile.objects.get_or_create(uuid=system_uuids.profile_uuid,creator=owner)[0]
        mprofile.system=True
        mprofile.name='Default Profile'
        mprofile.profile_id=system_uuids.profile_uuid
        mprofile.creator=owner
        mprofile.save()
        
        # Create it's dynapage node FOR PROFILE DISPLAY:
        template = Templates.objects.get(template_id=settings.PLY_DYNAPAGES_PROFILE_TEMPLATE)
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Node...'))
        mpage = Page.objects.get_or_create(page_id=system_uuids.profile_dynapage_uuid,creator=owner,template=template)[0]
        mpage.slug=system_uuids.profile_dynapage_uuid
        mpage.label="Magic Profile Template Node"

        mpage.save()
        
        # Add a basic Header Widget to the dynapage template:
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Node Widgets...'))
        widget = Widget.objects.get(widget_id=settings.PLY_DYNAPAGES_PROFILE_TEMPLATE_BANNER_WIDGET)
        widget.save()
        pageWidget = PageWidget.objects.get_or_create(page_id=mpage.page_id,widget=widget,banner=True)[0]
        pageWidget.save()

        # Create it's dynapage node FOR DASHBOARD DISPLAY:
        template = Templates.objects.get(template_id=settings.PLY_DYNAPAGES_DASHBOARD_TEMPLATE)
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Dashboard Node...'))
        mpage = Page.objects.get_or_create(page_id=system_uuids.pdashboard_dynapage_uuid,creator=owner,template=template)[0]
        mpage.slug=system_uuids.pdashboard_dynapage_uuid
        mpage.label="Magic Profile Template Node"
        mpage.save()

        # Add a basic Header Widget to the dynapage template:
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Dashboard Node Widgets...'))
        widget = Widget.objects.get(widget_id=settings.PLY_DYNAPAGES_DASHBOARD_TEMPLATE_BANNER_WIDGET)
        widget.save()
        pageWidget = PageWidget.objects.get_or_create(page_id=mpage.page_id,widget=widget,banner=True)[0]
        pageWidget.save()


        # Create the Dynapage node for INSTALL COMPLETE Splash:
        template = Templates.objects.get(template_id=settings.PLY_DYNAPAGES_INSTALL_COMPLETE_TEMPLATE)
        self.stdout.write(self.style.SUCCESS('Creating Dynapage "Install Complete" Coverpage Node...'))
        mpage = Page.objects.get_or_create(page_id=system_uuids.install_complete_uuid,creator=owner,template=template)[0]
        mpage.slug=system_uuids.install_complete_uuid
        mpage.label="Magic Dynapage Install Complete Coverpage Node"
        mpage.template=template
        mpage.save()

        self.stdout.write(self.style.SUCCESS('Success!'))

from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os

from dynapages.models import Templates,Page,Widget,PageWidget
from profiles.models import Profile


class Command(BaseCommand):
    help = 'Creates the empty magical \"system\" profile that will hold a blank DynaPage template that will be applied to all created profiles and groups. THIS SHOULD ONLY BE DONE ONCE PER SETUP!'


    def handle(self, *args, **options):
        # All profiles must be owned by the primary admin:
        owner = User.objects.get(is_superuser=True)
        
        # Create the magic Profile in the System:
        self.stdout.write(self.style.SUCCESS('Creating Magic profile...'))
        mprofile = Profile.objects.get_or_create(uuid=system_uuids.profile_uuid,system=True,name='Default Profile',profile_id=system_uuids.profile_uuid,creator=owner)[0]
        mprofile.save()
        
        # Create it's dynapage node FOR PROFILE DISPLAY:
        template = Templates.objects.get(template_id=settings.PLY_DYNAPAGES_PROFILE_TEMPLATE)
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Node...'))
        mpage = Page.objects.get_or_create(page_id=system_uuids.profile_dynapage_uuid,slug=system_uuids.profile_dynapage_uuid,label="Magic Profile Template Node",creator=owner,template=template)[0]
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
        mpage = Page.objects.get_or_create(page_id=system_uuids.pdashboard_dynapage_uuid,slug=system_uuids.profile_dynapage_uuid,label="Magic Profile Template Node",creator=owner,template=template)[0]
        mpage.save()

        # Add a basic Header Widget to the dynapage template:
        self.stdout.write(self.style.SUCCESS('Creating Magic Dynapage Profile Dashboard Node Widgets...'))
        widget = Widget.objects.get(widget_id=settings.PLY_DYNAPAGES_DASHBOARD_TEMPLATE_BANNER_WIDGET)
        widget.save()
        pageWidget = PageWidget.objects.get_or_create(page_id=mpage.page_id,widget=widget,banner=True)[0]
        pageWidget.save()

        self.stdout.write(self.style.SUCCESS('Success!'))

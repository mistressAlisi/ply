
import uuid
from django.contrib.auth.models import User
import os,pytz,datetime

from django.core.management.base import BaseCommand, CommandError
from ply import system_uuids,settings
from preferences.models import Timezone

class Command(BaseCommand):
    help = 'Populates the Timezone Table with options from the local pytz module: THIS SHOULD ONLY BE DONE ONCE PER SETUP!'


    def handle(self, *args, **options):
        # All profiles must be owned by the primary admin:


        # Add a basic Header Widget to the dynapage template:
        self.stdout.write(self.style.SUCCESS('Creating Timezone Objects....'))
        for tzi in pytz.common_timezones:
            dto = datetime.datetime.now(pytz.timezone(tzi))
            #print(dto.strftime("%Z"))
            tzo = Timezone.objects.get_or_create(tz=dto.strftime('%Z'),timezone=tzi,offset=dto.strftime('%z'),active=True)[0]
            tzo.save()
        #widget = Widget.objects.get(widget_id=settings.PLY_DYNAPAGES_PROFILE_TEMPLATE_BANNER_WIDGET)
        #widget.save()
        #pageWidget = PageWidget.objects.get_or_create(page_id=mpage.page_id,widget=widget,banner=True)[0]
        #pageWidget.save()

        self.stdout.write(self.style.SUCCESS('Success!'))

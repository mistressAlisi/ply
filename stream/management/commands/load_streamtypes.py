from django.core.management.base import BaseCommand, CommandError
import uuid
from ply import system_uuids,settings
import os,csv
from stream.models import StreamType
from community.models import Community

class Command(BaseCommand):
    help = 'Import a given pipe "|" separated file with  Stream Types to use in Streams / Game rooms'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if (os.path.exists(path)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'Loading Stream Types from {path}...'))
            with open(path) as file:
                comms = Community.objects.filter(archived=False,frozen=False)
                tsv_file = csv.reader(file, delimiter="|")
                for line in tsv_file:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Stream Type: "{line[0]}/{line[1]} being loaded...'))
                    for community in comms:
                        self.stdout.write(self.style.SUCCESS(f"Creating in Community: '{community.name}'...."))
                        cstty = StreamType.objects.get_or_create(community=community,name=line[0],descr=line[1])[0]
                        cstty.save()
        else:
            self.stdout.write(self.style.ERROR(f'NO SUCH File: \'{path}\'!'))
            return False
        self.stdout.write(self.style.SUCCESS('Success!'))


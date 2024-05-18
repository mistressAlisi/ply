from django.core.management.base import BaseCommand
import os,csv
from communities.community.models import CommunityDashboardType

class Command(BaseCommand):
    help = 'Import a given pipe "|" separated file with  Dashboard Types for use in Dashboard select and URL building. RUN THIS if your install is new!'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if (os.path.exists(path)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'Loading Dashboard Types from {path}...'))
            with open(path) as file:
                tsv_file = csv.reader(file, delimiter="|")
                for line in tsv_file:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Dashboard Type: "{line[0]}" ({line[1]}): Privileged: {line[3]}"...'))
                    dshb = CommunityDashboardType.objects.get_or_create(type=line[0])[0]
                    dshb.name = line[1]
                    dshb.descr = line[2]
                    dshb.privileged = line[3]
                    dshb.save()


        else:
            self.stdout.write(self.style.ERROR(f'NO SUCH File: \'{path}\'!'))
            return False


        self.stdout.write(self.style.SUCCESS('Success!'))


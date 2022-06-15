from django.core.management.base import BaseCommand, CommandError
import uuid
from ply import system_uuids,settings
import os,csv
from categories.models import Discipline
from profiles.models import Profile


class Command(BaseCommand):
    help = 'Import a given Pipe "|" separated file with Disciplines for the Categories in the Gallery.'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if (os.path.exists(path)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'Loading Disciplines from {path}...'))
            with open(path) as file:
                tsv_file = csv.reader(file, delimiter="|")
                for line in tsv_file:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Discipline: "{line[0]}/#{line[1]}"...'))
                    do = Discipline.objects.get_or_create(hash=line[1])
                    if (do[1] is True):
                         do[0].name = line[0]
                    do[0].save()
        else:
            self.stdout.write(self.style.ERROR(f'NO SUCH File: \'{path}\'!'))
            return False


        self.stdout.write(self.style.SUCCESS('Success!'))


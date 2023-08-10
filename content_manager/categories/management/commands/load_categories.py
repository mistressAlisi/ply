from django.core.management.base import BaseCommand
import os,csv
from content_manager.categories.models import Discipline,Category


class Command(BaseCommand):
    help = 'Import a given pipe "|" separated file with  Categories for use in in the Gallery - INSTALL DISCIPLINES FIRST'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if (os.path.exists(path)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'Loading Categories from {path}...'))
            with open(path) as file:
                tsv_file = csv.reader(file, delimiter="|")
                for line in tsv_file:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Category: "{line[1]}/#{line[2]} in Discipline {line[0]}"...'))
                    do = Discipline.objects.get(hash=line[0])
                    ca = Category.objects.get_or_create(hash=line[2],discipline=do)
                    if (ca[1] is True):
                         ca[0].name = line[1]
                    ca[0].save()
        else:
            self.stdout.write(self.style.ERROR(f'NO SUCH File: \'{path}\'!'))
            return False


        self.stdout.write(self.style.SUCCESS('Success!'))


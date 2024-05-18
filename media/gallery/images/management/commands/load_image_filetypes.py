from django.core.management.base import BaseCommand
import os,csv
from media.gallery.images.models import GalleryImagesFileTypes

class Command(BaseCommand):
    help = 'Import a given pipe "|" separated file with  allowed Image filetypes for use in in the Gallery Photo Plugin'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if (os.path.exists(path)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'Loading Image Filetypes from {path}...'))
            with open(path) as file:
                tsv_file = csv.reader(file, delimiter="|")
                for line in tsv_file:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Filetype: "{line[0]}/{line[1]}: {line[2]}"...'))
                    filetype = GalleryImagesFileTypes.objects.get_or_create(ext=line[0])[0]
                    filetype.mime = line[1]
                    filetype.name = line[2]
                    filetype.save()
        else:
            self.stdout.write(self.style.ERROR(f'NO SUCH File: \'{path}\'!'))
            return False


        self.stdout.write(self.style.SUCCESS('Success!'))


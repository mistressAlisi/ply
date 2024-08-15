from distutils.file_util import copy_file

from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os

from core.dynapages.models import Templates,Page,Widget,PageWidget
from communities.profiles.models import Profile


class Command(BaseCommand):
    help = 'Create the Ply Application Dashboards for the specified Django application - thus also making it a Ply app :)'


    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def _runner(self,src,dst):
        files = os.listdir(src)
        for file in files:

            if not os.path.exists(f"{dst}/{file}"):
                copy_file(f"{src}/{file}",f"{dst}/{file}")
            else:
                self.stdout.write(self.style.WARNING(f"File {dst}/{file} already exists."))
    def handle(self, *args, **options):
        app_name = options["app"]
        self.stdout.write(self.style.MIGRATE_HEADING(f"Copying Dashboard files from ../pytemplates/app_dashboards to {app_name}..."))
        src_path = os.getcwd() + f"/devtools/app_dev/pytemplates/app_dashboards"
        dst_path = os.getcwd() + f"/{app_name.replace('.','/')}"
        if os.path.isdir(src_path):
            self._runner(src_path,dst_path)
        else:
            src_path = os.getcwd() + f"/ply/devtools/app_dev/pytemplates/app_dashboards"
            if os.path.isdir(src_path):
                self._runner(src_path,dst_path)



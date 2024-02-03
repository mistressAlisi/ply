from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from bs4 import BeautifulSoup
import uuid
from ply import system_uuids,settings
from django.contrib.auth.models import User
import os
import ply



class Command(BaseCommand):
    help = 'Installs (runs) all the files in each app''s ''sql'' directory in order: Use ''_all_'' to specify all apps. If an APP is specified as an argument, only that app''s files are installed.'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)

    def run_dir(self,app):
        sql_dir  = os.getcwd() + f"/{app.replace('.','/')}/sql/"
        if (os.path.isdir(sql_dir)):
            self.stdout.write(self.style.MIGRATE_HEADING(f'...Installing files in: "{sql_dir}"...'))
            sqlfiles =  os.listdir(sql_dir)
            with connection.cursor() as cursor:
                for sql in sqlfiles:
                    self.stdout.write(self.style.MIGRATE_LABEL(f'Installing file "{sql}"...'))
                    sqlfile = open(sql_dir+"/"+sql).read()
                    cursor.execute(sqlfile)
            cursor.close()


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Installing SQL Files...'))
        if (options['app'] == '_all_'):
            for iapp in ply.settings.INSTALLED_APPS:
                self.run_dir(iapp)
        else:
            if (options['app'] in ply.settings.INSTALLED_APPS):
                self.run_dir(options['app'])
            else:
                self.stdout.write(self.style.ERROR(f'NO SUCH APP: \'{options["app"]}\'!'))
                return False


        self.stdout.write(self.style.SUCCESS('Success!'))

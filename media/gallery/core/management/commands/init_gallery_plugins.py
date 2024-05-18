import importlib

from django.core.management.base import BaseCommand
import os, csv
import ply
from communities.community.models import CommunityDashboardType
from media.gallery.core.models import GalleryPlugins


class Command(BaseCommand):
    help = "Scan all installed apps, finding gallery plugins and installing or updating them in the database: Use _all_ for all apps or specify the app name you wish!"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def process_app(self, app):
        try:
            module = importlib.import_module(f"{app}.gallery_plugin")
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    f'...Installing/updating Plugin in: "{app}"...'
                )
            )
            module_info = GalleryPlugins.objects.get_or_create(
                app=module.gallery_plugin["app"]
            )[0]
            module_info.name = module.gallery_plugin["name"]
            module_info.settings_model = module.gallery_plugin["settings_model"]
            module_info.descr = module.gallery_plugin["descr"]
            module_info.author = module.gallery_plugin["author"]
            module_info.version = module.gallery_plugin["version"]
            module_info.url = module.gallery_plugin["url"]
            module_info.repo = module.gallery_plugin["repo"]
            module_info.save()
        except ModuleNotFoundError:
            self.stdout.write(
                self.style.WARNING(
                    f"Application '{app}' does not have a gallery_plugin module/class..."
                )
            )
            pass
        # app_dir  = os.getcwd() + f"/{app.replace('.','/')}/sql/"
        # if (os.path.isdir(app_dir)):
        #     self.stdout.write(self.style.MIGRATE_HEADING(f'...Installing files in: "{app_dir}"...'))
        #     sqlfiles =  os.listdir(app_dir)
        #     with connection.cursor() as cursor:
        #         for sql in sqlfiles:
        #             self.stdout.write(self.style.MIGRATE_LABEL(f'Installing file "{sql}"...'))
        #             sqlfile = open(app_dir+"/"+sql).read()
        #             cursor.execute(sqlfile)
        #     cursor.close()

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Installing/updating Gallery plugins..."))
        if options["app"] == "_all_":
            for iapp in ply.settings.INSTALLED_APPS:
                self.process_app(iapp)
        else:
            if options["app"] in ply.settings.INSTALLED_APPS:
                self.process_app(options["app"])
            else:
                self.stdout.write(
                    self.style.ERROR(f'NO SUCH APP: \'{options["app"]}\'!')
                )
                return False

        self.stdout.write(self.style.SUCCESS("Success!"))

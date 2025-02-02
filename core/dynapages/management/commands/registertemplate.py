from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.dynapages.models import Templates
from bs4 import BeautifulSoup
import os
import ply


class Command(BaseCommand):
    help = "Registers all DynaPage templates in the /templates/dynapages/ dir in every app into the database"

    def register_template_file(self, file, template, app):
        soup = BeautifulSoup(file, "html.parser")
        name_prop = soup.find("meta", property="dynapage_template_name")
        author_prop = soup.find("meta", property="dynapage_template_author")
        descr_prop = soup.find("meta", property="dynapage_template_description")
        for_pages = False
        for_widgets = False
        type_prop = soup.find("meta", property="dynapage_template_type")
        if type_prop:
            if type_prop["content"] == "pages":
                for_pages = True
                for_widgets = False
            elif type_prop["content"] == "widgets":
                for_pages = False
                for_widgets = True
        if type(name_prop) == None:
            self.stdout.write(
                self.style.ERROR(
                    'Template "%s" is missing meta property "dynapage_template_name".'
                    % template
                )
            )
        else:
            tid = template.split(".")[0]
            template_obj = Templates.objects.get_or_create(template_id=tid)[0]
        if author_prop is not None:
            template_obj.filename = template
            template_obj.creator = author_prop["content"]
            template_obj.label = name_prop["content"]
            template_obj.description = descr_prop["content"]
            template_obj.app = app
            template_obj.page_template = for_pages
            template_obj.widget_template = for_widgets
            template_obj.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully registered Template "{template}" for Application "{app}"'
                )
            )

        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Skipped resgistering Template "{template}" for Application "{app}" - Metadata block not found in file.'
                )
            )
    def _runner(self,template_dir,app):
        templates = os.listdir(template_dir)
        for template in templates:
            tfile = open(template_dir + "/" + template)
            self.register_template_file(tfile, template, app)
    def handle(self, *args, **options):
        # Find all templates:
        for app in settings.INSTALLED_APPS:
            template_dir = os.getcwd() + f"/{app.replace('.','/')}/templates/dynapages"
            if os.path.isdir(template_dir):
                self._runner(template_dir,app)
            else:
                template_dir = os.getcwd() + f"/ply/{app.replace('.', '/')}/templates/dynapages"
                if os.path.isdir(template_dir):
                    self._runner(template_dir, app)


from django.core.management.base import BaseCommand, CommandError
from dynapages.models import Templates
from bs4 import BeautifulSoup
import os

class Command(BaseCommand):
    help = 'Registers all DynaPage templates in the templates/ into the database'


    def handle(self, *args, **options):
        # Find all templates:
        template_dir  = os.getcwd() + "/dynapages/templates"
        templates =  os.listdir(template_dir)

        for template in templates:
            tfile = open(template_dir+"/"+template)
            soup = BeautifulSoup(tfile,'html.parser')
            name_prop = soup.find("meta", property="dynapage_template_name")
            author_prop = soup.find("meta", property="dynapage_template_author")
            descr_prop = soup.find("meta", property="dynapage_template_description")
            if (type(name_prop) == None):
                self.stdout.write(self.style.ERROR('Template "%s" is missing meta property \"dynapage_template_name\".' % template))
            else:
                tid = (template.split(".")[0])
                template_obj = Templates.objects.get_or_create(template_id=tid)[0]
                if author_prop is not None:
                    template_obj.filename = template
                    template_obj.creator = author_prop["content"] 
                    template_obj.label = name_prop["content"]
                    template_obj.description = descr_prop["content"] 
                    template_obj.save()
                    self.stdout.write(self.style.SUCCESS('Successfully registered template "%s"' % template))

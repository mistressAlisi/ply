from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.dynapages.models import Templates
from bs4 import BeautifulSoup
import os
import json
import uuid
import ply
from core.dynapages.models import Widget,Templates
class Command(BaseCommand):
    help = 'Registers all DynaPage Widgets from the  dynapages/widgets/ dir in every app  into the database'
    def _runner(self,widget_dir,app):
        widgets = os.listdir(widget_dir)
        for widget in widgets:
            wfile = open(widget_dir + "/" + widget)
            try:
                wdata = json.load(wfile)
                try:
                    template = Templates.objects.get(template_id=wdata["dynapage_template"])
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Widget "{widget}" Needs Template: "{wdata["dynapage_template"]}"'))
                    self.stdout.write("Hint: Try registering the templates first with ./managepy registertemplate ;)")
                    print(e)
                    return False
                widget_obj = Widget.objects.get_or_create(widget_id=wdata["widget_name"], widget_name=wdata["widget_name"], author=wdata["author"], version=wdata["version"], label=wdata["title"], descr=wdata["descr"], helptext=wdata["helptext"], template=template, banner=wdata["modes"]["banner"], mainbody=wdata["modes"]["mainbody"], sidecol=wdata["modes"]["sidecol"], footer=wdata["modes"]["footer"])[0]
                if "used_in" in wdata:
                    widget_obj.profile = wdata["used_in"]["profile"]
                    widget_obj.SLHUD = wdata["used_in"]["SLHUD"]
                    widget_obj.group = wdata["used_in"]["group"]
                    widget_obj.dashboard = wdata["used_in"]["dashboard"]
                    widget_obj.blog = wdata["used_in"]["blog"]
                    if "staff" in wdata["used_in"]:
                        widget_obj.staff = wdata["used_in"]["staff"]
                if "icon" in wdata:
                    widget_obj.icon = wdata["icon"]
                if "system" in wdata:
                    widget_obj.system = wdata["system"]
                if "setup_required" in wdata:
                    widget_obj.setup_required = wdata["setup_required"]
                    widget_obj.setup_form = wdata["setup_form"]
                widget_obj.app = app
                widget_obj.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully registered/updated Widget "{widget}" for Application "{app}"'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Widget {widget} Fails registration: {e}'))
                print(e)

    def handle(self, *args, **options):
        # Find all widgets:
        for app in settings.INSTALLED_APPS:
            widget_dir  = os.getcwd() + f"/{app.replace('.','/')}/dynapages/widgets"
            if os.path.isdir(widget_dir):
                self._runner(widget_dir,app)
            else:
                widget_dir = os.getcwd() + f"/ply/{app.replace('.', '/')}/dynapages/widgets"
                if os.path.isdir(widget_dir):
                    self._runner(widget_dir, app)




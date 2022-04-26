from django.core.management.base import BaseCommand, CommandError
from dynapages.models import Templates
from bs4 import BeautifulSoup
import os
import json
import uuid
from dynapages.models import Widget,Templates
class Command(BaseCommand):
    help = 'Registers all DynaPage Widgets from the  default_widgets/ directory into the database'


    def handle(self, *args, **options):
        # Find all widgets:
        widget_dir  = os.getcwd() + "/dynapages/default_widgets"
        widgets =  os.listdir(widget_dir)

        for widget in widgets:
            wfile = open(widget_dir+"/"+widget)
            try: 
                wdata = json.load(wfile)
                try:
                    template = Templates.objects.get(template_id=wdata["dynapage_template"])
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Widget "{widget}" Needs Template: "{wdata["dynapage_template"]}"'))
                    print(e)
                    return False
                widget_obj = Widget(widget_id=wdata["widget_name"],widget_name=wdata["widget_name"],author=wdata["author"],version=wdata["version"],label=wdata["title"],descr=wdata["descr"],helptext=wdata["helptext"],template=template,banner=wdata["modes"]["banner"],mainbody=wdata["modes"]["mainbody"],sidecol=wdata["modes"]["sidecol"],footer=wdata["modes"]["footer"])
                widget_obj.save()
                self.stdout.write(self.style.SUCCESS('Successfully registered Widget "%s"' % widget))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Widget {widget} Fails registration: {e}'))
                print(e)

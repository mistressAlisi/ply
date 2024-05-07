from django.core.management.base import BaseCommand, CommandError
import uuid
from django.utils import timezone
from ply import system_uuids, settings, toolkit
from ply.models import PlyApplication
import importlib


class Command(BaseCommand):
    help = "Registers all applications that have a ply_appinfo (Ply Apps) class in the database; using this info to populate dashboard menus.."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("(re-)Registering New (and existing) PlyApps....")
        )
        major, minor, version = toolkit.version.get_featureset_version()
        self.stdout.write(
            self.style.SUCCESS(
                f"This cluster is running Ply Version {version}, with Feature Set Version: {major}.{minor}"
            )
        )

        for app in settings.INSTALLED_APPS:
            try:
                plyapp_info = importlib.import_module(f"{app}.ply_appinfo")
            except ModuleNotFoundError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Application: {app} is being ignored due to lack of ply_appinfo.py."
                    )
                )
                continue
            self.stdout.write(self.style.MIGRATE_HEADING(f"Application: {app} is being registered.."))
            major_ver_pass = (
                plyapp_info.PLY_APP_INFO["required_versions"]["featureset_major"]
                <= major
            )
            minor_ver_pass = (
                plyapp_info.PLY_APP_INFO["required_versions"]["featureset_minor"]
                <= minor
            )
            if (major_ver_pass == False) or (minor_ver_pass == False):
                self.stdout.write(
                    self.style.ERROR(
                        f'Error! Application: {app} requires Feature Set version:{plyapp_info.PLY_APP_INFO["required_versions"]["featureset_major"]}.{plyapp_info.PLY_APP_INFO["required_versions"]["featureset_minor"]}!'
                    )
                )
                return False
            appobj, created = PlyApplication.objects.get_or_create(
                app_module=plyapp_info.PLY_APP_INFO["app_module"]
            )
            _write = True
            if not created:
                appobj.updated = timezone.now()
                if (int(appobj.version_major)== plyapp_info.PLY_APP_INFO["version"]["major"]) and (int(appobj.version_minor)== plyapp_info.PLY_APP_INFO["version"]["minor"]):
                    self.stdout.write(self.style.SUCCESS(f"Application {app} is at the same version in registry; not registered."))
                    _write = False
                else:
                   appobj.updated = timezone.now()
                if _write:
                    appobj.app_name = plyapp_info.PLY_APP_INFO["app_name"]
                    appobj.version_release = plyapp_info.PLY_APP_INFO["version"]["release"]
                    appobj.version_major = plyapp_info.PLY_APP_INFO["version"]["major"]
                    appobj.version_minor = plyapp_info.PLY_APP_INFO["version"]["minor"]
                    appobj.save()
                    # for dm in plyapp_info.PLY_APP_INFO["dashboard_modes"]:
                    #     dto,created = PlyApplicationDashboardType.objects.get_or_create(application=appobj,mode=dm["mode"])
                    #     dto.default=dm["default"]
                    #     dto.active=dm["active"]
                    #     dto.privileged=dm["privileged"]
                    #     dto.descr=dm["descr"]
                    #     dto.menu_class=dm["menu_class"]
                    #     self.stdout.write(
                    #         self.style.MIGRATE_HEADING(f'Application {app}: Dashboard Type {dt["type"]} has been registered!')
                    #     )

                    self.stdout.write(
                        self.style.SUCCESS(f"Application {app} has been registered!")
                    )
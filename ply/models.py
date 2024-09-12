from django.db import models
from django.contrib import admin
import uuid


class PlyApplication(models.Model):
    class Meta:
        db_table = "ply_application"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    app_name = models.TextField(verbose_name="Application Name", blank=True)
    app_module = models.TextField(verbose_name="Application Module", unique=True)
    active = models.BooleanField(default=True)
    version_release = models.TextField(
        verbose_name="Application Module Release Version", default="0"
    )
    version_major = models.TextField(
        verbose_name="Application Module Major Version", default="0"
    )
    version_minor = models.TextField(
        verbose_name="Application Module Minor Version", default="0"
    )
    installed = models.DateTimeField(
        auto_now_add=True, verbose_name="Date Installed", blank=True
    )
    updated = models.DateTimeField(verbose_name="Date Updated", null=True, blank=True)

    def __str__(self):
        return f"Ply Application: {self.app_name}. Module: {self.app_module} Current Version: {self.version_major}.{self.version_minor}"


@admin.register(PlyApplication)
class PlyApplicationAdmin(admin.ModelAdmin):
    pass


class PlyApplicationVersionHistory(models.Model):
    class Meta:
        db_table = "ply_application_version_history"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    application = models.ForeignKey(
        PlyApplication, on_delete=models.CASCADE, verbose_name="Ply Application"
    )
    old_version_string = models.TextField(verbose_name="Application Old Version String")
    new_version_string = models.TextField(verbose_name="Application New Version String")
    updated = models.DateTimeField(auto_now=True, verbose_name="Date Updated")

    def __str__(self):
        return f"Ply Application: {self.app_name}. Upgrade from{self.old_version_string} -> {self.new_version_string} @ {self.updated}"


@admin.register(PlyApplicationVersionHistory)
class PlyApplicationVersionHistoryAdmin(admin.ModelAdmin):
    pass



# Generated by Django 5.0.1 on 2024-07-09 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_gallerytempfile_userdata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallerytempfile",
            name="userdata",
            field=models.JSONField(
                default={}, verbose_name="File User Review JSONData"
            ),
        ),
    ]

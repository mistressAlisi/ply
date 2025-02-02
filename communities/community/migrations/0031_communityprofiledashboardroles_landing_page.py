# Generated by Django 5.0.1 on 2024-05-11 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0030_delete_communityprofiledashboardroleswidgets"),
        ("dynapages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityprofiledashboardroles",
            name="landing_page",
            field=models.ForeignKey(
                help_text="This page will be loaded as a landing page of the dashboard mode for the given profile. (If default profile; it will be set as default for all subsequent profiles.)",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dynapages.page",
                verbose_name="Dashboard Landing Page Dynawidget Node",
            ),
        ),
    ]

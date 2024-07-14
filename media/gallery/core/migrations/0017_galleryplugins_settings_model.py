# Generated by Django 4.2.4 on 2024-04-26 05:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_galleryplugins_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryplugins",
            name="settings_model",
            field=models.CharField(
                default="", verbose_name="Application/plugin Settings Model"
            ),
            preserve_default=False,
        ),
    ]
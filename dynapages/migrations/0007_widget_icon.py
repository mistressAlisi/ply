# Generated by Django 4.0.4 on 2022-05-31 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynapages', '0006_widget_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='icon',
            field=models.TextField(blank=True, null=True, verbose_name='Widget Icon'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-12-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0015_rename_dasbhoard_type_communityprofiledashboardroles_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitydashboardtype',
            name='descr',
            field=models.TextField(default='', max_length=200, verbose_name='Dashboard Type Descr'),
            preserve_default=False,
        ),
    ]

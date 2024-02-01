# Generated by Django 4.2.4 on 2024-01-05 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0015_streamprofilexmppsettings_create_mucs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprofilexmppsettings',
            name='enable_webclient',
            field=models.BooleanField(default=True, help_text='Enable/disable the embedded XMPP client for all pages on the site.', verbose_name='Enable XMPP Webclient'),
        ),
    ]
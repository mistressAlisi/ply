# Generated by Django 4.0.2 on 2022-05-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0009_stream_default_perm'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='angle',
            field=models.IntegerField(default=90, verbose_name='Stream Bkg Midpoint '),
        ),
    ]

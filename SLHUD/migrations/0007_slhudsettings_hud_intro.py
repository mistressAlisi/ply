# Generated by Django 4.0.4 on 2022-07-08 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SLHUD', '0006_slhudsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='slhudsettings',
            name='hud_intro',
            field=models.TextField(default='', max_length=200, unique=True, verbose_name='HUD Introduction (World Name)'),
            preserve_default=False,
        ),
    ]

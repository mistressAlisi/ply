# Generated by Django 4.2.4 on 2023-08-15 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SLHUD', '0001_initial'),
        ('community', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='slparcel',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community'),
        ),
        migrations.AddField(
            model_name='slhudsettings',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community'),
        ),
        migrations.AddField(
            model_name='slagent',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community'),
        ),
        migrations.AddField(
            model_name='slagent',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]

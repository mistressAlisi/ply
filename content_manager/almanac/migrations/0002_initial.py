# Generated by Django 4.2.4 on 2023-08-15 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('almanac', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='almanacpage',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community'),
        ),
    ]

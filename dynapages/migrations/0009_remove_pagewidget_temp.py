# Generated by Django 4.0.4 on 2022-06-01 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynapages', '0008_pagewidget_active_pagewidget_temp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagewidget',
            name='temp',
        ),
    ]

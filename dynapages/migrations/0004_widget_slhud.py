# Generated by Django 4.0.4 on 2022-05-31 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynapages', '0003_widget_blog_widget_dashboard_widget_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='SLHUD',
            field=models.BooleanField(default=False, verbose_name='Includes SLHUD Mode'),
        ),
    ]

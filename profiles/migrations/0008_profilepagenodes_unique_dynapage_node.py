# Generated by Django 4.0.4 on 2022-08-10 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profilepagenodes'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='profilepagenodes',
            constraint=models.UniqueConstraint(fields=('profile', 'node_type'), name='unique_dynapage_node'),
        ),
    ]
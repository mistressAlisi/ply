# Generated by Django 4.0.2 on 2022-05-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_friend_friend1_remove_friend_friend2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notifications',
            field=models.IntegerField(default=0, verbose_name='Notification Count'),
        ),
    ]

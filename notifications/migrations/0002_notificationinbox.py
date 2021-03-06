# Generated by Django 4.0.2 on 2022-05-10 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_friend_community'),
        ('profiles', '0002_remove_friend_friend1_remove_friend_friend2_and_more'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationInbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Notification Inbox Created')),
                ('opened', models.DateTimeField(blank=True, null=True, verbose_name='Notification has been opened')),
                ('replied', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Notification has been replied to')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived FLAG')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden FLAG')),
                ('system', models.BooleanField(default=False, verbose_name='System FLAG')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted FLAG')),
                ('deleted_on', models.DateTimeField(editable=False, verbose_name='Notification Inbox Deleted on')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.notification', verbose_name='Notification')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='profiles.profile', verbose_name='Recipient Profile')),
            ],
        ),
    ]

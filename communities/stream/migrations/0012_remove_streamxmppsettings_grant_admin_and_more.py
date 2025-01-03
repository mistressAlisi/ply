# Generated by Django 4.2.4 on 2024-01-04 22:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('stream', '0011_streamprofilexmppsettings_unique_stream_xmpp_jid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamxmppsettings',
            name='grant_admin',
        ),
        migrations.RemoveField(
            model_name='streamxmppsettings',
            name='grant_admin2staff',
        ),
        migrations.RemoveField(
            model_name='streamxmppsettings',
            name='grant_mod',
        ),
        migrations.RemoveField(
            model_name='streamxmppsettings',
            name='grant_mod2staff',
        ),
        migrations.AlterField(
            model_name='streamxmppsettings',
            name='auto_group',
            field=models.BooleanField(default=True, help_text='Automatically create a MUC (Multi User Channel/Chat) for any created groups, streams, users, etc.', verbose_name='Automatic MUC for Groups'),
        ),
        migrations.AlterField(
            model_name='streamxmppsettings',
            name='self_reg',
            field=models.BooleanField(default=True, help_text='Allow users to register JIDs by themselves: UID@fqdn from their User Dashboard!', verbose_name='Enable User self-registration'),
        ),
        migrations.CreateModel(
            name='StreamProfileXMPPMUCs',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='Room Name')),
                ('service', models.TextField(verbose_name='Service Host FQDN')),
                ('host', models.TextField(verbose_name='Room Host/Virtual Host')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Settings Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Settings Updated')),
                ('XMPPJID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.streamprofilexmppsettings', verbose_name='Source XMPP JID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'db_table': 'communities_stream_stream_xmpp_profile_mucs',
            },
        ),
        migrations.AddConstraint(
            model_name='streamprofilexmppmucs',
            constraint=models.UniqueConstraint(fields=('name', 'service', 'host'), name='unique_stream_xmpp_muc'),
        ),
    ]

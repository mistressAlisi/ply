# Generated by Django 4.0.2 on 2022-04-26 13:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseStat',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='Name')),
                ('icon', models.TextField(blank=True, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Updated')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived FLAG')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked FLAG')),
                ('frozen', models.BooleanField(default=False, verbose_name='Frozen FLAG')),
                ('system', models.BooleanField(default=False, verbose_name='System FLAG')),
                ('minimum', models.IntegerField(default=0, verbose_name='Minimum Value')),
                ('maximum', models.IntegerField(default=10, verbose_name='Maximum Value')),
                ('starting', models.IntegerField(default=1, verbose_name='Starting Value')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileStatHistory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Updated')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked FLAG')),
                ('frozen', models.BooleanField(default=False, verbose_name='Frozen FLAG')),
                ('pminimum', models.IntegerField(default=0, verbose_name='Minimum Value')),
                ('pmaximum', models.IntegerField(default=10, verbose_name='Maximum Value')),
                ('value', models.IntegerField(default=1, verbose_name='Current Value')),
                ('notes', models.TextField(verbose_name='Name')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='profiles.profile', verbose_name='Profile')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.basestat', verbose_name='Community')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileStat',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Updated')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked FLAG')),
                ('frozen', models.BooleanField(default=False, verbose_name='Frozen FLAG')),
                ('pminimum', models.IntegerField(default=0, verbose_name='Minimum Value')),
                ('pmaximum', models.IntegerField(default=10, verbose_name='Maximum Value')),
                ('value', models.IntegerField(default=1, verbose_name='Current Value')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='profiles.profile', verbose_name='Profile')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.basestat', verbose_name='Community')),
            ],
        ),
    ]

# Generated by Django 4.0.4 on 2022-08-23 16:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0006_alter_communityprofile_profile'),
        ('plyscript', '0006_alter_script_function_name_alter_script_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1, verbose_name='Level (Numeric Value)')),
                ('name', models.TextField(verbose_name='Name')),
                ('expr', models.IntegerField(default=5, verbose_name='Experience Required')),
                ('statpoints', models.IntegerField(default=10, verbose_name='Stat Points Awarded')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Updated')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived FLAG')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked FLAG')),
                ('frozen', models.BooleanField(default=False, verbose_name='Frozen FLAG')),
                ('system', models.BooleanField(default=False, verbose_name='System FLAG')),
                ('starting', models.IntegerField(default=1, verbose_name='Starting Value')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community', verbose_name='Community')),
                ('script', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plyscript.script', verbose_name='Run Script on Awarding Level')),
            ],
        ),
    ]
# Generated by Django 4.0.4 on 2022-05-21 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0016_streammessage_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='streammessage',
            name='posted_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='stream.stream', verbose_name='Posted in Stream'),
        ),
    ]

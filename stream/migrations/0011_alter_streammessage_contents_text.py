# Generated by Django 4.0.2 on 2022-05-20 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0010_stream_angle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streammessage',
            name='contents_text',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Stream Content: Text Type'),
        ),
    ]
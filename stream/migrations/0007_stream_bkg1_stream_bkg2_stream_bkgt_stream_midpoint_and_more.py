# Generated by Django 4.0.2 on 2022-05-15 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0006_stream_group_stream_profile_stream_root_stream_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='bkg1',
            field=models.TextField(default='#ffffff', verbose_name='Stream Bkg Colour #1'),
        ),
        migrations.AddField(
            model_name='stream',
            name='bkg2',
            field=models.TextField(default='#ffffff', verbose_name='Stream Bkg Colour #2'),
        ),
        migrations.AddField(
            model_name='stream',
            name='bkgt',
            field=models.TextField(default='s1', verbose_name='Stream Bkg Type'),
        ),
        migrations.AddField(
            model_name='stream',
            name='midpoint',
            field=models.IntegerField(default=50, verbose_name='Stream Bkg Midpoint '),
        ),
        migrations.AddField(
            model_name='stream',
            name='opacity1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='Stream Bkg Opacity #1'),
        ),
        migrations.AddField(
            model_name='stream',
            name='opacity2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='Stream Bkg Opacity #2'),
        ),
    ]

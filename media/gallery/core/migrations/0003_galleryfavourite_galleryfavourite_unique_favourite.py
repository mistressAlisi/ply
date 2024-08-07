# Generated by Django 4.2.4 on 2023-08-15 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_initial'),
        ('profiles', '0001_initial'),
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryFavourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('archived', models.BooleanField(default=False, null=True, verbose_name='Archived FLAG')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden FLAG')),
                ('flagged', models.BooleanField(default=False, verbose_name='FLAGGED')),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='community.community', verbose_name='Community')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.galleryitem', verbose_name='Item')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='profiles.profile', verbose_name='Item')),
            ],
        ),
        migrations.AddConstraint(
            model_name='galleryfavourite',
            constraint=models.UniqueConstraint(fields=('item', 'profile', 'community'), name='unique_favourite'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-05-11 02:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dynapages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="slug",
            field=models.TextField(
                max_length=300, verbose_name="Page slug"
            ),
        ),
    ]
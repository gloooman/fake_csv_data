# Generated by Django 3.1.7 on 2021-02-23 20:46

import creator.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='path',
            field=models.FileField(blank=True, upload_to=creator.models.schema_directory_path, verbose_name='File path'),
        ),
    ]

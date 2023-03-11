# Generated by Django 4.1.7 on 2023-02-27 20:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_book_external_id_alter_book_published_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='authors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
    ]

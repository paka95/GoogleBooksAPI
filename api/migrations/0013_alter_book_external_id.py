# Generated by Django 4.1.7 on 2023-03-10 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_book_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='external_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

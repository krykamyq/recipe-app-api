# Generated by Django 3.2.23 on 2023-11-01 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='desctiption',
            new_name='description',
        ),
    ]

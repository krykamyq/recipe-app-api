# Generated by Django 3.2.23 on 2023-11-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20231101_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='link',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
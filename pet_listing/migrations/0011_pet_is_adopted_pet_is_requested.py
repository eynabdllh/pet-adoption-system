# Generated by Django 5.1.1 on 2024-11-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_listing', '0010_alter_pet_pet_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='is_adopted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pet',
            name='is_requested',
            field=models.BooleanField(default=False),
        ),
    ]

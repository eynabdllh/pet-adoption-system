# Generated by Django 5.1.1 on 2024-10-22 08:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_form', '0002_remove_adoption_adopter_id_adoption_adopter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoption',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
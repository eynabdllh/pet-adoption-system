# Generated by Django 5.1.1 on 2024-11-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_form', '0008_alter_schedule_reason_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.TimeField(),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_listing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='type',
        ),
        migrations.AddField(
            model_name='pet',
            name='description',
            field=models.TextField(default='No description available'),
        ),
        migrations.AddField(
            model_name='pet',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='pet_type',
            field=models.CharField(choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Bird', 'Bird'), ('Other', 'Other')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.ImageField(default='pet_images/default.png', upload_to='pet_images/'),
        ),
    ]
# Generated by Django 4.0.3 on 2023-05-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation_history', '0005_remove_violationhistory_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violationhistory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='violation/'),
        ),
    ]
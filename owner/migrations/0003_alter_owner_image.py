# Generated by Django 4.0.3 on 2023-05-11 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0002_owner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]

# Generated by Django 4.0.3 on 2023-05-15 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation_history', '0003_violationhistory_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='violationhistory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]

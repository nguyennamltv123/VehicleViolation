# Generated by Django 4.0.3 on 2023-05-10 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('violation_history', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='violationhistory',
            name='owner',
        ),
    ]
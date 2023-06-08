# Generated by Django 4.0.3 on 2023-06-05 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('violation_history', '0008_unsureviolationhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('fee', models.FloatField(default=5000000)),
            ],
        ),
        migrations.RemoveField(
            model_name='violationhistory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='violationhistory',
            name='fee',
        ),
        migrations.AddField(
            model_name='violationhistory',
            name='violation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='violation_history.violation'),
        ),
    ]
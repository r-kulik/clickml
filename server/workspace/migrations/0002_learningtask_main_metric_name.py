# Generated by Django 4.2.2 on 2023-07-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningtask',
            name='main_metric_name',
            field=models.CharField(default='Undefined', max_length=20),
        ),
    ]

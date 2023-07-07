# Generated by Django 4.2.2 on 2023-07-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodel',
            name='ready_for_usage',
            field=models.BooleanField(default=False, help_text='True if model was learned and is ready for expluatation'),
        ),
    ]
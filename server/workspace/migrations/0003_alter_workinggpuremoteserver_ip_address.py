# Generated by Django 4.2.2 on 2023-07-10 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_uploadtokens_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinggpuremoteserver',
            name='IP_ADDRESS',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

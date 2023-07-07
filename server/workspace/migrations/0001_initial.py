# Generated by Django 4.2.2 on 2023-07-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLMODEL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(help_text='Name of model', max_length=1000)),
                ('model_directory', models.CharField(help_text='Link to the ml model storing directory', max_length=1000)),
                ('owner_user_id', models.IntegerField(help_text='User id of models owner')),
            ],
        ),
    ]
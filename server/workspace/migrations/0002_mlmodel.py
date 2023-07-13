# Generated by Django 4.2.2 on 2023-07-11 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLMODEL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('config_best_json_file', models.FilePathField()),
                ('encoder_best_file', models.FilePathField()),
                ('scaler_best_file', models.FilePathField()),
                ('model_best_file', models.FilePathField()),
                ('creation_time', models.DateTimeField()),
                ('ready_to_use', models.BooleanField(default=False)),
                ('valid_token_to_upload_files', models.CharField(default='', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
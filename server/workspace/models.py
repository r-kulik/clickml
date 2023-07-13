from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=100)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class ModelOnCreation(models.Model):
    username = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    dataset_file_name = models.FilePathField()

    def deletePreviousIfExists(self) -> None:
        previousEntities = ModelOnCreation.objects.filter(username=self.username)
        for entity in previousEntities:
            entity.delete()


class LearningTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    task_type = models.CharField(max_length=100)
    target_variable = models.CharField(max_length=100)
    upload_token = models.CharField(max_length=100)
    GPU_server_IP = models.CharField(max_length=20)
    success = models.IntegerField()


class WorkingGpuRemoteServer(models.Model):
    IP_ADDRESS = models.CharField(max_length=20, unique=True)
    LAST_REQUEST = models.DateTimeField()


class UploadTokens(models.Model):
    FILE_PATH = models.FilePathField()
    UPLOAD_TOKEN = models.CharField(max_length=100)


class MLMODEL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    config_best_json_file = models.FilePathField()
    encoder_best_file = models.FilePathField()
    scaler_best_file = models.FilePathField()
    model_best_file = models.FilePathField()
    creation_time = models.DateTimeField()
    ready_to_use = models.BooleanField(default=False)
    valid_token_to_upload_files=models.CharField(max_length=100, default="")




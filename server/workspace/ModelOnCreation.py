from django.db import models


class ModelOnCreation(models.Model):
    username = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    dataset_file = models.FileField()

    def deletePreviousIfExists(self) -> None:
        previousEntities = ModelOnCreation.objects.filter(username=self.username)
        for entity in previousEntities:
            entity.delete()

from django.db import models

# Create your models here.
from django.urls import reverse


class MLMODEL(models.Model):

    model_name = models.CharField(
        help_text="Name of model",
        max_length=1000
    )

    model_directory = models.CharField(
        help_text = "Link to the ml model storing directory",
        max_length=1000
    )

    owner_user_id = models.IntegerField(
        help_text="User id of models owner"
    )

    ready_for_usage = models.BooleanField(
        help_text="True if model was learned and is ready for expluatation",
        default=False
    )

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.model_name
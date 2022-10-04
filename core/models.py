from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.CustomManager()

    class Meta:
        abstract = True

from django.db import models
from django.db.models import Manager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("Updated_at"))

    objects = Manager()

    class Meta:
        abstract = True
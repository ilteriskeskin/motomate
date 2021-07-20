from django.utils import timezone
from django.db import models

from core.models import BaseModel

class Tour(BaseModel):
    tour_name = models.CharField(max_length=255)
    from_city = models.CharField(max_length=255)# Buraya choices eklenecek ve ülkenin tüm şehirleri olacak.
    to_city = models.CharField(max_length=255)# Buraya choices eklenecek ve ülkenin tüm şehirleri olacak.
    tour_date = models.DateTimeField(default=timezone.now, verbose_name=("tour date"))
    note = models.TextField(verbose_name="Tour Note")

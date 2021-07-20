import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.models import BaseModel
from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name=("email address"))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=("date joined"))
    first_name = models.CharField(max_length=255, verbose_name=("first name"))
    last_name = models.CharField(max_length=255, verbose_name=("last name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=("birth date"))
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=("phone"))

    city = models.CharField(max_length=255, verbose_name="city") # Buraya choices eklenecek ve ülkenin tüm şehirleri olacak.
    motorcycle_brand = models.CharField(max_length=255, verbose_name="motorcycle brand")  
    engine_capacity = models.CharField(max_length=255, verbose_name="engine capacity")

    # Social Media
    twitter_username = models.CharField(max_length=255)
    instagram_username = models.CharField(max_length=255)
    telegram_username = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True, verbose_name="active")
    is_staff = models.BooleanField(default=False, verbose_name="staff status")

    objects = UserManager()

    USERNAME_FIELD = "email"

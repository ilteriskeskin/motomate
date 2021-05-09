from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Manager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("Updated_at"))

    objects = Manager()

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    is_active = models.BooleanField(default=True, verbose_name=("active"))
    is_staff = models.BooleanField(default=False, verbose_name=("staff status"))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=("date joined"))

    first_name = models.CharField(max_length=255, verbose_name=("first name"))
    last_name = models.CharField(max_length=255, verbose_name=("last name"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=("birth date"))
    
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=("phone"))
    twitter_username = models.CharField(max_length=255, verbose_name=("twitter username"))
    instagram_username = models.CharField(max_length=255, verbose_name=("instagram username"))
    telegram_username = models.CharField(max_length=255, verbose_name=("telegram username"))

    motorcycle_brand = models.CharField(max_length=255, verbose_name=("motorcycle brand"))
    engine_capacity = models.CharField(max_length=255, verbose_name=("engine capacity"))

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


    def __str__(self):
        return self.email
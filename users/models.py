from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="Логин")

    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

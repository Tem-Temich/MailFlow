from django.db import models
from django.conf import settings


# Create your models here.
class Client(models.Model):
    class Meta:
        permissions = [
            ("can_view_all_clients", "Can view all clients"),
        ]

    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    fio = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество")
    comments = models.TextField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец"
    )

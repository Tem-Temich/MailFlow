from django.db import models
from django.conf import settings


# Create your models here.

class Message(models.Model):
    class Meta:
        permissions = [
            ("can_view_all_messages", "Can view all messages"),
        ]

    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name="Содержание письма")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец"
    )

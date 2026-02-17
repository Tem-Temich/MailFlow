from django.db import models
from mail_messages.models import Message
from clients.models import Client
# Create your models here.
STATUS_CHOICES_MAILINGS = [
    ("created", "Создана"),
    ("started", "Запущена"),
    ("finished", "Завершена"),
]
STATUS_CHOICES_ATTEMPTS = [('succeeded','Успашно'), ('failed',"Не успешно")]


class Mailing(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES_MAILINGS,
        default="created"
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )

    clients = models.ManyToManyField(Client)

class Attempt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_ATTEMPTS)
    response = models.TextField(max_length=500,null=True,blank=True)
    mailings = models.ForeignKey(Mailing,on_delete=models.CASCADE,null=True,blank=True)

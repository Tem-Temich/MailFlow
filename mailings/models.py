from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from mail_messages.models import Message
from clients.models import Client
# Create your models here.

STATUS_CHOICES_ATTEMPTS = [('succeeded','Успешно'), ('failed',"Не успешно")]


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name='Начало рассылки')
    end_time = models.DateTimeField(verbose_name="Конец рассылки")

    @property
    def status(self):
        now=timezone.now()
        if now<self.start_time:
            return 'Создана'
        elif self.start_time <= now <= self.end_time:
            return "Запущена"
        else:
            return "Завершена"

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,verbose_name="Выбор сообщения для рассылки"
    )

    recipients = models.ManyToManyField(Client,verbose_name="Клиент получатель")

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    "Дата начала должна быть раньше даты окончания."
                )

            if self.start_time < timezone.now():
                raise ValidationError(
                    "Дата начала не может быть в прошлом."
                )

class Attempt(models.Model):
    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время отправки"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES_ATTEMPTS,
        verbose_name="Статус отправки"
    )

    server_response = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ответ почтового сервиса"
    )

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name="Рассылка"
    )

    def __str__(self):
        return f"{self.mailing} - {self.status}"
from django.db import models

# Create your models here.

class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name="Содержание письма")

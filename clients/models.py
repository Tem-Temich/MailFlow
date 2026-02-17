from django.db import models

# Create your models here.
class Client(models.Model):
    email = models.EmailField(max_length=100,unique=True,verbose_name="Email")
    fio = models.CharField(max_length=100,verbose_name="Фамилия Имя Отчество")
    comments = models.TextField(max_length=500,null=True,blank=True)
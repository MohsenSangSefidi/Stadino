from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserModels(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars', verbose_name='',)
    activeCode = models.CharField(max_length=20, verbose_name='')
    token = models.CharField(max_length=40, verbose_name='')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name= 'کاربر'
        verbose_name_plural= 'کاربران'
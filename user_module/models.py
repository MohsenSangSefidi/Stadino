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

class AddressModel(models.Model):
    user = models.ForeignKey(UserModels, on_delete=models.CASCADE, verbose_name='کاربر')
    address = models.CharField(max_length=100, verbose_name='address', null=True)
    detail = models.TextField(verbose_name='text', null=True)
    state = models.CharField(max_length=100, verbose_name='ostan', null=True)
    city = models.CharField(max_length=100, verbose_name='city', null=True)
    phone_number = models.CharField(max_length=100, verbose_name='phone', null=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')
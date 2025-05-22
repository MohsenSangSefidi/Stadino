from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'( Username: {self.username} - Email: {self.email} )'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=1500)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'( User : {self.user.username} - Phone Number: {self.phone_number} )'

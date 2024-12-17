from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"username: {self.username} - email: {self.email}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=1500)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)

    def __str__(self):
        return f"street: {self.street} - city: {self.city} - state:{self.state} - phone_number: {self.phone_number}"

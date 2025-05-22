from django.db import models


class Banners(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title

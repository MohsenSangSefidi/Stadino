from django.db import models
from users.models import User


class Product(models.Model):
    book_title = models.CharField(max_length=150)
    book_author = models.CharField(max_length=150)
    book_translator = models.CharField(max_length=150)
    book_page_count = models.IntegerField()
    book_price = models.IntegerField()
    book_description = models.TextField()
    book_slug = models.SlugField()
    book_image = models.ImageField(upload_to='products/')
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.book_title} - {self.book_author}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.product.book_title} - {self.id}'

class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_title = models.CharField(max_length=150)
    feature_description = models.TextField(max_length=150)

    def __str__(self):
        return f'{self.feature_title} - {self.product.book_title}'


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'

    def filled_star(self):
        return range(0, self.rating)

    def unfilled_star(self):
        unfilled = 5 - int(self.rating)
        return range(0, unfilled)
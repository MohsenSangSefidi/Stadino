from django.db import models
from users.models import User


class Category(models.Model):
    category_title = models.CharField(max_length=150)

    def __str__(self):
        return f'( Category : {self.category_title} )'


class Product(models.Model):
    book_title = models.CharField(max_length=150)
    book_author = models.CharField(max_length=150)
    book_translator = models.CharField(max_length=150)
    book_page_count = models.IntegerField()
    book_price = models.IntegerField()
    book_description = models.TextField()
    book_slug = models.SlugField()
    book_image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'( Product : {self.book_title} )'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'( Product Title : {self.product.book_title} - Image Path : {self.image.url} )'


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return f'( User : {self.user.username} - Product : {self.product.book_title} - Rating : {self.rating} )'

    def filled_star(self):
        return range(0, self.rating)

    def unfilled_star(self):
        unfilled = 5 - int(self.rating)
        return range(0, unfilled)


class DiscountedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounted_products')
    discounted_precentage = models.IntegerField()
    end_date = models.DateField()

    def __str__(self):
        return f'( Product Title : {self.product.book_title} - Discount : {self.discounted_precentage} )'

    def discounted_price(self):

        discounted_price = (self.product.book_price * self.discounted_precentage) / 100

        return discounted_price


class FavoriteProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite_products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')

    def __str__(self):
        return f'( Username: {self.user.username} - Favorite Product : {self.product.book_title} )'

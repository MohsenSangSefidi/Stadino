from django.db import models
from users.models import User
from jalali_core import GregorianToJalali

class Category(models.Model):
    category_title = models.CharField(max_length=150)

    def __str__(self):
        return f'Category : {self.category_title}'


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
    discounted_percentage = models.IntegerField(default=0)
    discounted_expire_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Product : {self.book_title}'

    # Return price after applying discount
    def discounted_price(self):
        if self.discounted_percentage:
            discounted_price = self.book_price - ((self.book_price * self.discounted_percentage) / 100)
        else:
            return None

        return int(discounted_price)

    # Return amount of discount
    def discount_amount(self):
        if self.discounted_percentage:
            discount_amount = (self.book_price * self.discounted_percentage) / 100
        else:
            return None

        return int(discount_amount)

    # Return discount date for showing on timer
    def discount_date(self):
        if self.discounted_expire_date:
            return f'{self.discounted_expire_date.year}-{self.discounted_expire_date.month}-{self.discounted_expire_date.day}'

        return None

    # Return discount time for showing on timer
    def discount_time(self):
        if self.discounted_expire_date:
            return f'{self.discounted_expire_date.hour}:{self.discounted_expire_date.minute}'

        return None

    # Return avrage rating for showing on template
    def average_rating(self):
        if self.comments.count() != 0:
            rating = []

            for rate in self.comments.all():
                rating.append(rate.rating)

            average_rating = sum(rating) / len(rating)

            return average_rating

        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'Product Title : {self.product.book_title} - Image Path : {self.image.url}'


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return f'User : {self.user.username} - Product : {self.product.book_title} - Rating : {self.rating}'

    # Return list of rate for showing star on comment section
    def filled_star(self):
        return range(0, self.rating)

    # Return list of rate for showing star on comment section
    def unfilled_star(self):
        unfilled = 5 - int(self.rating)
        return range(0, unfilled)

    # Return jalale date of create_at for showing on comment section
    def jalali_created_at(self):
        date = GregorianToJalali(self.created_at.year, self.created_at.month, self.created_at.day).getJalaliList()

        return f'{date[2]} / {date[1]} / {date[0]}'


class FavoriteProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite_products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')

    def __str__(self):
        return f'( Username: {self.user.username} - Favorite Product : {self.product.book_title} )'

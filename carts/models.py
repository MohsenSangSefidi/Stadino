from django.db import models
from jalali_core import GregorianToJalali

from products.models import Product
from users.models import User, Address


class DiscountCode(models.Model):
    discount_code = models.CharField(max_length=10)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Discount Code : {self.discount_code}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateField(auto_now_add=True)
    pay_amount = models.IntegerField(default=0)
    pay_date = models.DateField(null=True, blank=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='carts', null=True)
    is_paid = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='carts', null=True)
    cart_status = models.BooleanField(default=False)

    def __str__(self):
        return f'Username : {self.user.username} - Cart : {self.id}'

    def get_jalali_pay_date(self):
        if self.pay_date is not None:
            date = GregorianToJalali(self.pay_date.year, self.pay_date.month, self.pay_date.day).getJalaliList()

            return f'{date[2]} / {date[1]} / {date[0]}'

    def get_jalali_created_at(self):
        date = GregorianToJalali(self.created_at.year, self.created_at.month, self.created_at.day).getJalaliList()

        return f'{date[2]} / {date[1]} / {date[0]}'

    def total_amount_with_out_discount(self):
        total = 0

        for item in self.cart_item.all():
            total += item.product.book_price * item.quantity

        return total

    def total_discounted_amount(self):
        total = 0

        for item in self.cart_item.all():
            if item.product.discounted_percentage:
                total += item.product.discount_amount() * item.quantity

        return total

    def total_amount(self):

        total = self.total_amount_with_out_discount() - self.total_discounted_amount()

        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.IntegerField(default=1)
    pay_amount = models.IntegerField(default=0)

    def __str__(self):
        return f'Product : {self.product.book_title} - Quantity : {self.quantity}'

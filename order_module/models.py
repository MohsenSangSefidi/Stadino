from django.db import models

from product_module.models import ProductModel
from user_module.models import UserModels, AddressModel

# Create your models here.

class DiscountCodeModel(models.Model):
    code = models.CharField(max_length=100, verbose_name='کد')
    discount = models.IntegerField(verbose_name='تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

class OrderModel(models.Model):
    user = models.ForeignKey(UserModels, on_delete=models.CASCADE, verbose_name='کاربر')
    is_pay = models.BooleanField(default=False, verbose_name='پرداخت شده')
    pay_datetime = models.DateField(null=True, verbose_name='زمان پرداخت')
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, verbose_name='آدرس', null=True)
    delivery_type = models.CharField(max_length=100, verbose_name="نوع ارسال", null=True, default='normal')
    delivery_price = models.IntegerField(verbose_name="قیمت ارسال", null=True, default=10000)
    discount_code = models.ForeignKey(DiscountCodeModel,null=True,blank=True, on_delete=models.CASCADE, verbose_name='کد تخفیف')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def total_price(self):
        total = 0
        for item in self.orderdetailmodel_set.all():
            total += item.finalPrice()
        return total

    def total_discount(self):
        total = 0
        for item in self.orderdetailmodel_set.all():
            total += (item.product.disCoun_price() * item.count)
        return total

    def discount_code_price(self):
        total = 0
        for item in self.orderdetailmodel_set.all():
            total += item.finalPriceWithDiscount()
        total_with_discount = total - (((total) * self.discount_code.discount ) / 100)
        return int(total - total_with_discount)

    def total_with_delivery(self):
        if self.discount_code is None:
            total = 0
            for item in self.orderdetailmodel_set.all():
                total += item.finalPriceWithDiscount()
            return int(total)

        else:
            total = 0
            for item in self.orderdetailmodel_set.all():
                total += item.finalPriceWithDiscount()
            return int(total - (((total) * self.discount_code.discount) / 100))

class OrderDetailModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(verbose_name='قیمت نهایی')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'محصول سبد خرید'
        verbose_name_plural = 'محصول های سبد خرید'

    def finalPrice(self):
        return self.product.price * self.count

    def finalPriceWithDiscount(self):
        return self.product.disCount() * self.count
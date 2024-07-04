from django.contrib import admin
from .models import OrderModel, DiscountCodeModel, OrderDetailModel

# Register your models here.

admin.site.register(OrderModel)
admin.site.register(DiscountCodeModel)
admin.site.register(OrderDetailModel)
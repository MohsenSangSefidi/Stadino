from django.contrib import admin
from .models import Product, ProductImage, ProductComments, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'book_price', 'inventory', 'is_active')
    prepopulated_fields = {'book_slug': ('book_title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductComments)
admin.site.register(Category)

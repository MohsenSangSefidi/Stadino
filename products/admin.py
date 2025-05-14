from django.contrib import admin
from .models import Product, ProductImage, ProductFeatures, ProductComments


class ProductAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'book_price', 'inventory', 'is_active')
    prepopulated_fields = {'book_slug': ('book_title',)}


class ProductFeaturesAdmin(admin.ModelAdmin):
    list_display = ('feature_title', 'feature_description')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductFeatures, ProductFeaturesAdmin)
admin.site.register(ProductComments)

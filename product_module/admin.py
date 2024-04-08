from django.contrib import admin
from .models import *

# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'field', 'price', 'is_active']
    list_editable = ['price', 'is_active']
    prepopulated_fields = {
        'slug' : ['name', 'field']
    }

class CatgoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {
        'slug' : ['name']
    }

class PublisherModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {
        'slug' : ['name']
    }

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']

admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(CatgoryModel, CatgoryModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(ProductImageModel)
admin.site.register(CatgoryImageModel)
admin.site.register(PublisherModel, PublisherModelAdmin)
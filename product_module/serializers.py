from rest_framework import serializers
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    # publisher = serializers.SerializerMethodField(source='publisher')
    # catgory = serializers.SerializerMethodField(source='catgory')

    class Meta:
        model = ProductModel
        fields = [
            'id',
            'name',
            'field',
            'grade',
            'lesson',
            'publish_date',
            'cut',
            'cover',
            'count',
            'rating',
            'page',
            'price',
            'publisher',
            'detail',
            'is_active',
            'slug',
            'is_special',
            'discount',
            'special_discount_date',
            'disCount',
            'ratingAvrg',
            'disCoun_price'
        ]

    def get_publisher(self, obj):
        return {
            'name' : obj.publisher.name,
            'slug' : obj.publisher.slug
        }

    # def get_catgory(self, obj):
    #     list = []
    #     for item in obj.catgory.all():
    #         dict = {
    #             'name' : item.name,
    #             'parent' : item.parent,
    #             'slug' : item.slug
    #         }
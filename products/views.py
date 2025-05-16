from django.shortcuts import render, redirect, reverse
from django.views import View

from .models import Product, ProductComments, FavoriteProducts


class ProductView(View):
    def get(self, request, slug, *args, **kwargs):

        try:
            product_object = Product.objects.prefetch_related('comments', 'images').get(book_slug=slug)
        except Product.DoesNotExist:
            return redirect(reverse('index'))

        favorite_products = False

        try:
            FavoriteProducts.objects.get(product=product_object, user=request.user)
            favorite_products = True
        except FavoriteProducts.DoesNotExist:
            favorite_products = False

        comments = product_object.comments.all()

        images = product_object.images.all()

        return render(
            request, 'product.html', {
                'object': product_object,
                'comments': comments,
                'images': images,
                'favorite_products': favorite_products
            }
        )

    def post(self, request, slug, *args, **kwargs):
        comment = request.POST.get('comment')
        rating = request.POST['rating']

        product_object = Product.objects.filter(book_slug=slug).only('id').first()

        comment_object = ProductComments.objects.create(
            product_id=product_object.id,
            user_id=request.user.id,
            rating=rating,
            comment=comment,
        )

        return redirect(reverse('product-view', kwargs={'slug': slug}))


def add_favorite(request, slug):
    product_object = Product.objects.get(book_slug=slug)

    FavoriteProducts.objects.create(product_id=product_object.id, user_id=request.user.id,)

    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)


def remove_favorite(request, slug):
    product_object = Product.objects.get(book_slug=slug)

    FavoriteProducts.objects.get(product_id=product_object.id, user_id=request.user.id).delete()

    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)

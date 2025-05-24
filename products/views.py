from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views import View

from .models import Product, ProductComments, FavoriteProducts


class ProductView(View):
    def get(self, request, slug, *args, **kwargs):
        # Trying to get product object ( if didn't exist, returns previous-page )
        try:
            product_object = Product.objects.prefetch_related('comments', 'images').get(book_slug=slug)
        except Product.DoesNotExist:
            # Return previous-page
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        # Check if product in user favorite products variables
        favorite_products = False

        # Trying to Check if product in user favorite products
        try:
            FavoriteProducts.objects.get(product=product_object, user=request.user)
            favorite_products = True
        except:
            favorite_products = False

        # Get all products comments
        comments = product_object.comments.all()

        # Get all product image
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
        # Get information from request.POST ( Saving comments )
        comment = request.POST.get('comment')
        rating = request.POST['rating']

        # Trying to get product object ( If didn't exist, returns previous-page )
        try:
            product_object = Product.objects.get(book_slug=slug)

        except Product.DoesNotExist:
            # Return previous-page
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        # Create comment object
        comment_object = ProductComments.objects.create(
            product_id=product_object.id,
            user_id=request.user.id,
            rating=rating,
            comment=comment,
        )

        return redirect(reverse('product-view', kwargs={'slug': slug}))


# Function for add product to user favorite product
@login_required()
def add_favorite(request, slug):
    # Trying to get product object ( If didn't exist, returns previous-page )
    try:
        product_object = Product.objects.get(book_slug=slug)

    except Product.DoesNotExist:
        # Return previous-page
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    # Add product to favorite products
    FavoriteProducts.objects.create(product_id=product_object.id, user_id=request.user.id,)

    # Return previous-page
    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)

# Function for remove product to user favorite product
@login_required()
def remove_favorite(request, slug):
    # Trying to get product object ( If didn't exist, returns previous-page )
    try:
        product_object = Product.objects.get(book_slug=slug)

    except Product.DoesNotExist:
        # Return previous-page
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    # Remove product to favorite products
    FavoriteProducts.objects.get(product_id=product_object.id, user_id=request.user.id).delete()

    # Return previous-page
    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)

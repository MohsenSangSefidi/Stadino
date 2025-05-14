from django.shortcuts import render, redirect, reverse
from django.views import View

from .models import Product, ProductComments


class ProductView(View):
    def get(self, request, slug, *args, **kwargs):

        product_object = Product.objects.filter(book_slug=slug).prefetch_related('comments').first()
        comments = product_object.comments.all()

        return render(
            request, 'product.html', {
                'object': product_object,
                'comments': comments,
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

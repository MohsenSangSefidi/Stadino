from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.views import View

from carts.views import create_cart
from products.models import Product, Category


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html')


class SearchProductView(View):
    def get(self, request, searched_content, *args, **kwargs):
        filters = {
            'book_title__icontains': searched_content,
        }

        products = Product.objects.filter(**filters).only(
            'book_title', 'book_price', 'discounted_percentage'
        ).prefetch_related('comments')

        order_by = request.GET.get('order_by')

        if order_by:
            products = products.order_by(order_by)

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price and max_price:
            products = products.filter(book_price__gte=min_price, book_price__lte=max_price)

        paginator = Paginator(products, 10)

        page = request.GET.get('page')
        paginated_products = paginator.page(page if page else 1)

        return render(
            request, 'search_products.html', {
                'paginated_products': paginated_products,
                'searched_content': searched_content,
                'order_by': order_by,
            }
        )

    def post(self, request, searched_content, *args, **kwargs):

        min_price = request.POST.get('min')
        max_price = request.POST.get('max')
        order_by = request.GET.get('order_by')

        url = reverse('search', kwargs={'searched_content': searched_content})
        params = {
            'min_price': min_price,
            'max_price': max_price,
        }

        if order_by:
            params['order_by'] = order_by

        return redirect(f'{url}?{urlencode(params)}')


class HeaderView(View):
    def get(self, request, *args, **kwargs):
        cart_item_count = 0

        if request.user.is_authenticated:
            cart_item_count = create_cart(request).cart_item.count()

        return render(
            request, 'header.html', {
                'cart_item_count': cart_item_count
            }
        )

    def post(self, request, *args, **kwargs):
        searched_content = request.POST.get('searched_content')

        return redirect(reverse('search', kwargs={'searched_content': searched_content}))


class FooterView(View):
    def get(self, request, *args, **kwargs):
        cart_items = None

        if request.user.is_authenticated:
            cart = create_cart(request)

            cart_items = cart.cart_item.only(
                'product__book_title', 'product__book_price',
                'product__inventory', 'product__book_image',
                'product__book_slug'
            )

        return render(
            request, 'footer.html', {
                'cart_items': cart_items,
            }
        )

    def post(self, request, *args, **kwargs):
        cart_items = None

        if request.user.is_authenticated:
            cart = create_cart(request)

            cart_items = cart.cart_item.only(
                'product__book_title', 'product__book_price',
                'product__inventory', 'product__book_image',
                'product__book_slug'
            )

        return render(
            request, 'footer.html', {
                'cart_items': cart_items,
            }
        )

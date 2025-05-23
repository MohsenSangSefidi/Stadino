from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.utils import timezone
from django.views import View

from carts.views import create_cart
from products.models import Product, Category
from .models import Banners


class IndexView(View):
    def get(self, request, *args, **kwargs):

        banners = Banners.objects.only('image', 'url').all()

        discounted_products = Product.objects.filter(is_active=True).exclude(discounted_percentage=0).only(
            'book_title', 'book_image', 'book_price', 'book_slug', 'discounted_percentage', 'discounted_expire_date'
        ).exclude(discounted_expire_date__lte=timezone.now())[:10]

        categories = Category.objects.all()

        favorite_products = []

        if request.user.is_authenticated:
            favorite_products = [
                item.product.book_title for item in request.user.favorite_products.only('product__book_title').all()
            ]

        products_in_categories = []

        for category in categories[:4]:
            products_in_categories.append(
                {
                    'category_title': category.category_title,
                    'products': category.products.only(
                        'book_title', 'book_image', 'book_price', 'book_slug', 'discounted_percentage',
                        'discounted_expire_date'
                    ).all()[:10]
                }
            )

        return render(
            request, 'index.html', {
                'products_in_categories': products_in_categories,
                'discounted_products': discounted_products,
                'favorite_products': favorite_products,
                'categories': categories,
                'banners': banners,
            }
        )

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html')


class SearchProductView(View):
    def get(self, request, searched_content, *args, **kwargs):
        filters = {
            'book_title__icontains': searched_content if searched_content != 'all' else '',
        }

        params = {}

        filter_status = {

        }

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price and max_price:
            filters['book_price__gte'] = min_price
            filters['book_price__lte'] = max_price

            params['min_price'] = min_price
            params['max_price'] = max_price

            filter_status['price'] = 'price'

        category_title = request.GET.get('category_title')

        if category_title:
            category = Category.objects.get(category_title=category_title)

            filters['category'] = category

            params['category_title'] = category_title

            filter_status['category'] = 'category'

        products = Product.objects.filter(**filters).only(
            'book_title', 'book_price', 'discounted_percentage'
        ).prefetch_related('comments')

        order_by = request.GET.get('order_by')

        if order_by:
            products = products.order_by(order_by)
            filter_status['order_by'] = 'order_by'

        paginator = Paginator(products, 10)

        page = request.GET.get('page')
        paginated_products = paginator.page(page if page else 1)

        categories = Category.objects.all()

        order_by_persian = ''

        match order_by:
            case '-book_price':
                order_by_persian = 'گران ترین'
            case 'book_price':
                order_by_persian = 'ارزان ترین'
            case '-created_at':
                order_by_persian = 'داغ ترین'

        return render(
            request, 'search_products.html', {
                'paginated_products': paginated_products,

                'searched_content': searched_content,

                'filter_status': filter_status,

                'url_prams': urlencode(params),

                'categories': categories,

                'category_title': category_title,
                'min_price': min_price,
                'max_price': max_price,
                'order_by': order_by,

                'order_by_persian': order_by_persian,
            }
        )

    def post(self, request, searched_content, *args, **kwargs):

        min_price = request.POST.get('min')
        max_price = request.POST.get('max')

        category_title = request.GET.get('category_title')
        order_by = request.GET.get('order_by')

        url = reverse('search', kwargs={'searched_content': searched_content})
        params = {
            'min_price': min_price,
            'max_price': max_price,
        }

        if order_by:
            params['order_by'] = order_by

        if category_title:
            params['category_title'] = category_title

        return redirect(f'{url}?{urlencode(params)}')


class HeaderView(View):
    def get(self, request, *args, **kwargs):
        cart_item_count = 0

        if request.user.is_authenticated:
            cart_item_count = create_cart(request).cart_item.count()

        categories = Category.objects.all()

        return render(
            request, 'header.html', {
                'cart_item_count': cart_item_count,
                'categories': categories,
            }
        )

    def post(self, request, *args, **kwargs):
        searched_content = request.POST.get('searched_content')

        return redirect(reverse('search', kwargs={'searched_content': searched_content}))


class FooterView(View):
    def get(self, request, *args, **kwargs):
        cart_items = None
        favorite_products_count = None

        if request.user.is_authenticated:
            favorite_products_count = request.user.favorite_products.count()
            cart = create_cart(request)

            cart_items = cart.cart_item.only(
                'product__book_title', 'product__book_price',
                'product__inventory', 'product__book_image',
                'product__book_slug'
            )

        return render(
            request, 'footer.html', {
                'cart_items': cart_items,
                'favorite_products_count': favorite_products_count
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


def filter_by_category(request, searched_content):
    if request.method == 'POST':

        category_title = request.POST.get('category')

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        order_by = request.GET.get('order_by')

        url = reverse('search', kwargs={'searched_content': searched_content})

        params = {
            'category_title': category_title,
        }

        if order_by and order_by != 'None':
            params['order_by'] = order_by

        if min_price and max_price:
            params['min_price'] = min_price
            params['max_price'] = max_price

        return redirect(f'{url}?{urlencode(params)}')


def remove_filter(request, searched_content, filter_name):
    category_title = request.GET.get('category_title')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    order_by = request.GET.get('order_by')

    url = reverse('search', kwargs={'searched_content': searched_content})
    params = {}

    if category_title:
        params['category_title'] = category_title

    if min_price and max_price:
        params['min_price'] = min_price
        params['max_price'] = max_price

    if order_by and order_by != 'None':
        params['order_by'] = order_by

    match filter_name:
        case 'category':
            params.pop('category_title')
        case 'price':
            params.pop('min_price')
            params.pop('max_price')
        case 'order_by':
            params.pop('order_by')

    return redirect(f'{url}?{urlencode(params)}')

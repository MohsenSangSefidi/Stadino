from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, InvalidPage
from urllib.parse import urlencode
from django.utils import timezone
from django.views import View

from carts.views import create_cart
from products.models import Product, Category
from .models import Banners


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Get banner with only required fields
        banners = Banners.objects.only('image', 'url').all()

        # Get discounted product with only required field and exclude product with expired discount
        discounted_products = Product.objects.filter(is_active=True).exclude(discounted_percentage=0).only(
            'book_title', 'book_image', 'book_price', 'book_slug', 'discounted_percentage', 'discounted_expire_date'
        ).exclude(discounted_expire_date__lte=timezone.now())[:10]

        # Get all category
        categories = Category.objects.all()

        # This list for saving user favorite product to comparison in template
        favorite_products = []

        # Get user favorite product if user is authenticated
        if request.user.is_authenticated:
            # Write a for loop in line for saving all favorite product title in list
            favorite_products = [
                item.product.book_title for item in request.user.favorite_products.only('product__book_title').all()
            ]

        # A list for sort some products and category for showing on template
        products_in_categories = []

        for category in categories[:4]:
            # For 4 category add 10 products to the list for showing on page ( Just gets required fields )
            products_in_categories.append(
                {
                    'category_title': category.category_title,
                    'products': category.products.only(
                        'book_title', 'book_image', 'book_price', 'book_slug', 'discounted_percentage',
                        'discounted_expire_date'
                    ).all()[:10]
                }
            )

        #
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
        # This dict for save what user want to search
        filters = {
            'book_title__icontains': searched_content if searched_content != 'all' else '',
        }

        # This dict for saving Query-Params for requesting to another page in template
        params = {}

        # This dict for changing page number in template
        params_change_page = {}

        # This dict for showing what type filter applying on Query
        filter_status = {

        }

        # Get Information from Query-Params ( For price filter )
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Check if variables are valid
        if min_price and max_price:
            # Add variables to filters dict
            filters['book_price__gte'] = min_price
            filters['book_price__lte'] = max_price

            # Add variables to Query-Params
            params['min_price'] = min_price
            params['max_price'] = max_price

            # Add variables to Query-Params
            params_change_page['min_price'] = min_price
            params_change_page['max_price'] = max_price

            # Add variables filter-status dict
            filter_status['price'] = 'price'

        # Get Information from Query-Params ( For category filter )
        category_title = request.GET.get('category_title')

        # Check if variable are valid
        if category_title:
            # Trying to get category information
            try:
                category = Category.objects.get(category_title=category_title)

                # Add variables to filters dict
                filters['category'] = category

                # Add variables to Query-Params
                params['category_title'] = category_title

                # Add variables to Query-Params
                params_change_page['category_title'] = category_title

                # Add variables filter-status dict
                filter_status['category'] = 'category'

            except Category.DoesNotExist:
                pass

        # Get and filtering products
        products = Product.objects.filter(**filters).only(
            'book_title', 'book_price', 'discounted_percentage'
        ).prefetch_related('comments')

        # Get Information from Query-Params ( For sorting filter )
        order_by = request.GET.get('order_by')

        # Check if variable are valid
        if order_by:
            # Sorting products
            products = products.order_by(order_by)

            # Add variables to Query-Params
            params_change_page['order_by'] = order_by

            # Add variables filter-status dict
            filter_status['order_by'] = 'order_by'

        # Paginate Products
        paginator = Paginator(products, 10)

        # Get Information from Query-Params ( Page number )
        page = request.GET.get('page')

        if page:
            params['page'] = page

        try:
            # Paginate by page number ( If page number didn't send, returns page 1 )
            paginated_products = paginator.page(page if page else 1)
        except InvalidPage:
            # Paginate by page number ( If page didn't exist, returns page 1 )
            paginated_products = paginator.page(1)
            params['page'] = 1

        # Get all categories for showing on filter list
        categories = Category.objects.all()

        # This variable is used to indicate the sort type.
        order_by_persian = ''

        # Set value for variable
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
                'filter_status': filter_status,

                # For request another page
                'url_prams': urlencode(params),
                'params_change_page': params_change_page,
                'searched_content': searched_content,

                # For show categories in filter list
                'categories': categories,

                # For showing filter list
                'category_title': category_title,
                'min_price': min_price,
                'max_price': max_price,
                'order_by': order_by,
                'order_by_persian': order_by_persian,
            }
        )

    def post(self, request, searched_content, *args, **kwargs):

        # Get information from request.POST ( For price filter )
        min_price = request.POST.get('min')
        max_price = request.POST.get('max')

        # Get Information from Query-Params ( Filters that have already been applied )
        category_title = request.GET.get('category_title')
        order_by = request.GET.get('order_by')
        page = request.GET.get('page')

        # Set url and Query-Params for redirect
        url = reverse('search', kwargs={'searched_content': searched_content})
        params = {
            'min_price': min_price,
            'max_price': max_price,
        }

        # Check if variable are valid
        if order_by:
            # Add variable to Query-Params
            params['order_by'] = order_by

        # Check if variable are valid
        if page:
            # Add variable to Query-Params
            params['page'] = page

        # Check if variable are valid
        if category_title:
            # Add variable to Query-Params
            params['category_title'] = category_title

        return redirect(f'{url}?{urlencode(params)}')


class HeaderView(View):
    def get(self, request, *args, **kwargs):
        # User shopping cart item count
        cart_item_count = 0

        # Set cart_item_count if user authenticated
        if request.user.is_authenticated:
            cart_item_count = create_cart(request).cart_item.count()

        # Get all categories showing on header
        categories = Category.objects.all()

        return render(
            request, 'header.html', {
                'cart_item_count': cart_item_count,
                'categories': categories,
            }
        )

    def post(self, request, *args, **kwargs):
        # User shopping cart item count
        cart_item_count = 0

        # Set cart_item_count if user authenticated
        if request.user.is_authenticated:
            cart_item_count = create_cart(request).cart_item.count()

        # Get all categories showing on header
        categories = Category.objects.all()

        return render(
            request, 'header.html', {
                'cart_item_count': cart_item_count,
                'categories': categories,
            }
        )


class FooterView(View):
    def get(self, request, *args, **kwargs):
        # Get cart-item for showing on template
        cart_items = None
        # Get user favorite products count for showing on footer ( Just showing on mobile )
        favorite_products_count = None

        # Set variables if user authenticated
        if request.user.is_authenticated:
            favorite_products_count = request.user.favorite_products.count()

            # Get user Current-Cart
            cart = create_cart(request)

            # Get cart items and save them
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
        # Get cart-item for showing on template
        cart_items = None
        # Get user favorite products count for showing on footer ( Just showing on mobile )
        favorite_products_count = None

        # Set variables if user authenticated
        if request.user.is_authenticated:
            favorite_products_count = request.user.favorite_products.count()

            # Get user Current-Cart
            cart = create_cart(request)

            # Get cart items and save them
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


def filter_by_category(request, searched_content):
    if request.method == 'POST':
        # Get information from request.POST ( For category filter )
        category_title = request.POST.get('category')

        # Get Information from Query-Params ( Filters that have already been applied )
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        order_by = request.GET.get('order_by')
        page = request.GET.get('page')

        # Set url and Query-Params for redirect
        url = reverse('search', kwargs={'searched_content': searched_content})
        params = {
            'category_title': category_title,
        }

        # Check if variable valid
        if order_by and order_by != 'None':
            # Add variable to Query-Params
            params['order_by'] = order_by

        # Check if variable are valid
        if page:
            # Add variable to Query-Params
            params['page'] = page

        # Check if variables valid
        if min_price and max_price:
            # Add variables to Query-Params
            params['min_price'] = min_price
            params['max_price'] = max_price

        return redirect(f'{url}?{urlencode(params)}')


def remove_filter(request, searched_content, filter_name):
    # Get Information from Query-Params ( Filters that have already been applied )
    category_title = request.GET.get('category_title')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    order_by = request.GET.get('order_by')
    page = request.GET.get('page')

    # Set url and Query-Params for redirect
    url = reverse('search', kwargs={'searched_content': searched_content})
    params = {}

    # Check if variable valid
    if category_title:
        # Add variable to Query-Params
        params['category_title'] = category_title

    # Check if variable valid
    if min_price and max_price:
        # Add variable to Query-Params
        params['min_price'] = min_price
        params['max_price'] = max_price

    # Check if variable valid
    if order_by and order_by != 'None':
        # Add variable to Query-Params
        params['order_by'] = order_by

    # Check if variable are valid
    if page:
        # Add variable to Query-Params
        params['page'] = page

    # Compare the submitted filter name with the filters applied to the products to remove filters
    match filter_name:
        case 'category':
            params.pop('category_title')
        case 'price':
            params.pop('min_price')
            params.pop('max_price')
        case 'order_by':
            params.pop('order_by')

    return redirect(f'{url}?{urlencode(params)}')


# Function for send user to search page
def search_view(request):
    if request.method == 'POST':
        # Get information from request.POST
        searched_content = request.POST.get('searched_content')

        return redirect(reverse('search', kwargs={'searched_content': searched_content}))

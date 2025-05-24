from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from carts.models import Cart, CartItem
from products.models import Product
from users.models import Address


# Function for getting user Current-Cart ( If didn't exist, it creates that )
def create_cart(request):
    try:
        # Get shopping cart information
        cart = Cart.objects.get(user=request.user, is_paid=False)
        return cart

    except Cart.DoesNotExist:
        # Creating shopping cart, if didn't exist
        cart = Cart.objects.create(
            user=request.user,
        )
        return cart


@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request, *args, **kwargs):
        # Get user Current-Cart
        cart = create_cart(request)

        # Get cart-item with only required fields
        cart_items = cart.cart_item.only(
            'product__book_title', 'product__inventory', 'product__book_slug', 'product__book_image'
        )

        return render(
            request, 'cart.html', {
                'cart': cart,
                'cart_items': cart_items,
            }
        )


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        # Get user Current-Cart
        cart = create_cart(request)

        # Get user address information from request.user
        address = request.user.address.filter(is_active=True)

        return render(
            request, 'checkout.html', {
                'cart': cart, 'address': address,
            }
        )

    def post(self, request, *args, **kwargs):
        # Get user Current-Cart
        cart = create_cart(request)

        # Get address.id from request.POST
        selected_address_id = request.POST.get('address')

        # Try to get address object ( If address didn't exist, return previous-page )
        try:
            address = Address.objects.get(pk=selected_address_id)

        except Address.DoesNotExist:
            # Get previous-page from request
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        # Save address information in cart
        cart.address = address
        cart.save()

        return redirect('success_payment')


@method_decorator(login_required, name='dispatch')
class SuccessPaymentView(View):
    def get(self, request, *args, **kwargs):
        # Get user Current-Cart
        cart = create_cart(request)

        # Save payment status in cart
        cart.pay_date = timezone.now()
        cart.is_paid = True
        cart.save()

        # Save new inventory amount of product after shopping
        for cart_item in cart.cart_item.all():
            # Get products information
            product = cart_item.product

            # Calculate new inventory amount
            new_inventory = (product.inventory - cart_item.quantity)

            # Set new inventory amount
            product.inventory = new_inventory if new_inventory > 0 else 0

            # Save that
            product.save()

        return render(request, 'success_payment.html')


@method_decorator(login_required, name='dispatch')
class CartDetailView(View):
    def get(self, request, cart_id, *args, **kwargs):
        # Trying to get cart object ( If didn't exist, returns previous-page )
        try:
            cart = Cart.objects.get(pk=cart_id)

        except Cart.DoesNotExist:
            # Return previous-page
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        return render(
            request, 'cart_detail.html', {
                'cart': cart,
            }
        )


# A function for add product to Current-Cart ( I used this view on javascript - main.js )
@login_required()
def add_to_cart(request):
    # Get user Current-Cart
    cart = create_cart(request)

    # Get information from Query-Prams
    product_slug = request.GET.get('product_slug')
    quantity = request.GET.get('quantity')

    # Trying to get product object ( If didn't exist, returns Error )
    try:
        product = Product.objects.get(book_slug=product_slug)

    except Product.DoesNotExist:
        return JsonResponse(
            {'status': 'error'}
        )

    # Trying fet Cart-Object & Update it ( If didn't exist, it creates that with information )
    try:
        # Get cart & Save information
        cart_item = CartItem.objects.get(cart_id=cart.id, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        # Create cart
        cart_items = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity
        )

    # Rendering some part of template for replacing new information
    factor_section_html = render_to_string(
        'factor_section.html', {'cart': cart}
    )

    # Returning JsonResponse because I used it in javascript ( main.js )
    return JsonResponse({'status': 'success', 'value': quantity, 'factor_section': factor_section_html})


# Function for remove product from Current-Cart
@login_required()
def remove_from_cart(request):
    # Get user Current-Cart
    cart = create_cart(request)

    # Get information from Query-Params
    product_slug = request.GET.get('product_slug')

    # Trying to get product object ( If didn't exist, returns previous-page )
    try:
        product = Product.objects.get(book_slug=product_slug)

    except Product.DoesNotExist:
        # Get previous-page from request
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    # Trying to get Cart-Item object & Delete that ( If didn't exist, returns previous-page )
    try:
        cart_item = CartItem.objects.get(cart_id=cart.id, product=product)
        cart_item.delete()

    except CartItem.DoesNotExist:
        # Get previous-page from request
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    # Returning previous-page
    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)

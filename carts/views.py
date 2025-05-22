from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from carts.models import Cart, CartItem
from products.models import Product
from users.models import Address


def create_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        return cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user=request.user,
        )
        return cart


@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = create_cart(request)

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
        cart = create_cart(request)

        address = request.user.address.filter(is_active=True)

        return render(
            request, 'checkout.html', {
                'cart': cart, 'address': address,
            }
        )

    def post(self, request, *args, **kwargs):
        cart = create_cart(request)

        selected_address_id = request.POST.get('address')

        try:
            address = Address.objects.get(pk=selected_address_id)
        except Address.DoesNotExist:
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        cart.address = address
        cart.save()

        return redirect('success_payment')


@method_decorator(login_required, name='dispatch')
class SuccessPaymentView(View):
    def get(self, request, *args, **kwargs):
        cart = create_cart(request)

        cart.pay_date = timezone.now()
        cart.is_paid = True
        cart.save()

        for cart_item in cart.cart_item.all():
            product = cart_item.product

            new_inventory = (product.inventory - cart_item.quantity)

            product.inventory = new_inventory if new_inventory > 0 else 0

            product.save()

        return render(request, 'success_payment.html')


@method_decorator(login_required, name='dispatch')
class CartDetailView(View):
    def get(self, request, cart_id, *args, **kwargs):
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        return render(
            request, 'cart_detail.html', {
                'cart': cart,
            }
        )


@login_required()
def add_to_cart(request):
    cart = create_cart(request)

    product_slug = request.GET.get('product_slug')
    quantity = request.GET.get('quantity')

    try:
        product = Product.objects.get(book_slug=product_slug)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error'})

    try:
        cart_item = CartItem.objects.get(cart_id=cart.id, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_items = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity
        )

    factor_section_html = render_to_string(
        'factor_section.html', {'cart': cart}
    )

    return JsonResponse({'status': 'success', 'value': quantity, 'factor_section': factor_section_html})


@login_required()
def remove_from_cart(request):
    cart = create_cart(request)

    product_slug = request.GET.get('product_slug')

    try:
        product = Product.objects.get(book_slug=product_slug)
    except Product.DoesNotExist:
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    try:
        cart_item = CartItem.objects.get(cart_id=cart.id, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)

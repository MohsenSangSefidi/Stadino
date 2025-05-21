from django.urls import path
from .views import CartView, add_to_cart, remove_from_cart, CheckoutView, SuccessPaymentView, CartDetailView

urlpatterns = [

    # Class Base View
    path('view_cart/', CartView.as_view(), name='carts'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success_payment/', SuccessPaymentView.as_view(), name='success_payment'),
    path('cart_detial/<cart_id>', CartDetailView.as_view(), name='cart_detail'),

    # Function Base View
    path('add-cart-item/', add_to_cart, name='add-cart-item'),
    path('remove-cart-item', remove_from_cart, name='remove-cart-item'),

]

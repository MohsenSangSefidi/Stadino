from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-order/', add_to_order, name='add-to-order'),
    path('basket/', UserBasket.as_view(), name='basket'),
    path('remove_product/', remove_product, name='remove-product-from-basket'),
    path('change-count/', change_count, name='change-count'),
    path('check-out/', CheckOutView.as_view(), name='checkout'),
    path('success-pay/', SuccessPayment.as_view(), name="success-pay")
]
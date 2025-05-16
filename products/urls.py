from django.urls import path
from .views import ProductView, add_favorite, remove_favorite

urlpatterns = [
    path('<slug:slug>', ProductView.as_view(), name='product-view'),
    path('favorite-products/add/<slug:slug>', add_favorite, name='add-favorite'),
    path('favorite-products/remove/<slug:slug>', remove_favorite, name='remove-favorite'),
]

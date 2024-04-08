from django.urls import path
from .views import *

urlpatterns = [
    path('<slug>/', ProductDetailView.as_view(), name='product-detail')
]
from django.urls import path
from .views import *

urlpatterns = [
    path('search/all/', SearchPageAllView.as_view(), name='search-all'),
    path('search/all/<start>/<end>/', SearchPageAllPriceFilterView.as_view(), name='search-all-price-filter'),
    path('search/all/<catgory>/', SearchPageAllCatgoryFilterView.as_view(), name='search-all-catgory-filter'),
    path('search/product/<name>/', SearchPageView.as_view(), name='search'),
    path('search/product/<name>/<start>/<end>/', SearchPagePriceFileterView.as_view(), name='search-price-filter'),
    path('search/product/<name>/<catgory>', SearchPageCatgoryFileterView.as_view(), name='search-catgory-filter'),
    path('search/catgory/<catgory>/', SearchPageCatgoryView.as_view(), name='search-catgory'),
    path('search/catgory/<catgory>/<start>/<end>/', SearchPageCatgoryPriceFilterView.as_view(), name='search-catgory-price-filter'),
    path('detial/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-product-to-favorite/', add_product_to_favorite, name='add-product-to-favorite'),
    path('product-api/', ProductApiView.as_view(), name='product-api')
]
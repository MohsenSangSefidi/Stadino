from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('search/all/', SearchPageAllView.as_view(), name='search-all'),
    path('search/all/<start>/<end>/', SearchPageAllPriceFilterView.as_view(), name='search-all-price-filter'),
    re_path(r'search/all/(?P<catgory>[^/]+)/?$', SearchPageAllCatgoryFilterView.as_view(), name='search-all-catgory-filter'),
    re_path(r'search/product/(?P<name>[^/]+)/?$', SearchPageView.as_view(), name='search'),
    re_path(r'search/product/(?P<name>[^/]+)/(?P<start>[^/]+)/(?P<end>[^/]+)/', SearchPagePriceFileterView.as_view(), name='search-price-filter'),
    re_path(r'search/product/(?P<name>[^/]+)/(?P<catgory>[^/]+)/?$', SearchPageCatgoryFileterView.as_view(), name='search-catgory-filter'),
    re_path(r'search/catgory/(?P<catgory>[^/]+)/?$', SearchPageCatgoryView.as_view(), name='search-catgory'),
    re_path(r'search/catgory/(?P<catgory>[^/]+)/(?P<start>[^/]+)/(?P<end>[^/]+)/', SearchPageCatgoryPriceFilterView.as_view(), name='search-catgory-price-filter'),
    re_path(r'detial/(?P<slug>[^/]+)/?$', ProductDetailView.as_view(), name='product-detail'),
    path('add-product-to-favorite/', add_product_to_favorite, name='add-product-to-favorite'),
    path('product-api/', ProductApiView.as_view(), name='product-api')
]



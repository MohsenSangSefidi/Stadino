from django.urls import path
from .views import HeaderView, FooterView, IndexView, SearchProductView, filter_by_category, remove_filter

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/<str:searched_content>', SearchProductView.as_view(), name='search'),

    path('header/', HeaderView.as_view(), name='header'),
    path('footer/', FooterView.as_view(), name='footer'),

    path('filter_by_category/<str:searched_content>', filter_by_category, name='filter_by_category'),
    path('remove_filter/<str:searched_content>/<str:filter_name>', remove_filter, name='remove_filter'),
]

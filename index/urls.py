from django.urls import path
from .views import HeaderView, FooterView, IndexView, SearchProductView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/<str:searched_content>', SearchProductView.as_view(), name='search'),

    path('header/', HeaderView.as_view(), name='header'),
    path('footer/', FooterView.as_view(), name='footer'),
]

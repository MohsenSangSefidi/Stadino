from django.urls import path
from .views import HeaderView, FooterView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('header/', HeaderView.as_view(), name='header'),
    path('footer/', FooterView.as_view(), name='footer'),
]

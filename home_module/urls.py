from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeViews.as_view(), name='home'),
]
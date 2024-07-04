import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View

from order_module.models import OrderModel, OrderDetailModel
from product_module.models import CatgoryModel, ProductModel, FavoriteProduct, ProductSliderModel
from .forms import SearchForm


# Create your views here.

class HomeViews(View):
    def get(self, request: HttpRequest):
        product = ProductModel.objects.filter(is_active=True, discount=0)[0:10]
        special_discount = ProductModel.objects.filter(is_special=True, is_active=True)
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)

        for item in special_discount:
            if item.special_discount_date <= datetime.datetime.date(datetime.datetime.now()):
                item.is_special = False
                item.save()

        special_discount_product = ProductModel.objects.filter(is_special=True, is_active=True)

        slider = ProductSliderModel.objects.all()
        catgory = CatgoryModel.objects.filter(parent=None)
        return render(request, 'home.html', {
            'products': product,
            'catgorys': catgory,
            'special': special_discount_product,
            'favorit' : favoritProduct,
            'slider' : slider
        })

    def post(self, request: HttpRequest):
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            return redirect(reverse('search', args=[text]))

class HeaderView(View):
    def get(self, request: HttpRequest):
        form = SearchForm()
        category = CatgoryModel.objects.filter(parent=None)
        if request.user.is_authenticated:
            basket = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
            if basket is not None:
                basket_count = OrderDetailModel.objects.filter(order_id=basket.id)
                return render(request, 'header.html', {
                    'category': category,
                    'count': basket_count.count(),
                    'form': form
                })
            else:
                return render(request, 'header.html', {
                    'category': category,
                    'form': form
                })
        else:
            return render(request, 'header.html', {
                'category': category,
                'form': form
            })

    def post(self, request: HttpRequest):
        form = SearchForm()
        category = CatgoryModel.objects.filter(parent=None)
        if request.user.is_authenticated:
            basket = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
            if basket is not None:
                basket_count = OrderDetailModel.objects.filter(order_id=basket.id)
                return render(request, 'header.html', {
                    'category': category,
                    'count': basket_count.count(),
                    'form': form
                })
            else:
                return render(request, 'header.html', {
                    'category': category,
                    'form': form
                })
        else:
            return render(request, 'header.html', {
                'category': category,
                'form': form
            })

def footerView(request: HttpRequest):
    category = CatgoryModel.objects.filter(parent=None)
    return render(request, 'footer.html', {
        'category' : category
    })

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from product_module.models import CatgoryModel, ProductModel

# Create your views here.

class HomeViews(View):
    def get(self, request:HttpRequest):
        product = ProductModel.objects.filter(is_active=True, discount=None)[0:10]
        discountproduct = ProductModel.objects.filter(is_active=True, discount__isnull=False)[0:10]
        catgory = CatgoryModel.objects.filter(parent=None)
        return render(request, 'home.html', {
            'products' : product,
            'discount' : discountproduct,
            'catgorys' : catgory
        })

def headerView(request:HttpRequest):
    category = CatgoryModel.objects.filter(parent=None)
    return render(request, 'header.html', {
        'category' : category
    })

def footerView(request:HttpRequest):
    return render(request, 'footer.html')
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from rest_framework.views import APIView, Response
from home_module.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from .models import *
from .forms import *

# Create your views here.
from django.views.generic import ListView
from django.views import View


class ProductDetailView(View):
    def get(self, request: HttpRequest, slug):
        product = ProductModel.objects.filter(slug=slug).first()
        comments = product.commentmodel_set.filter(parent=None)
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        form = CommentForm()
        return render(request, 'product-detail.html', {
            'product': product,
            'form': form,
            'comments': comments,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, slug):
        product = ProductModel.objects.filter(slug=slug).first()
        form = CommentForm(request.POST)

        if form.is_valid():
            rating = 0
            if form.cleaned_data.get('rating1'):
                rating = form.cleaned_data.get('rating1')
            elif form.cleaned_data.get('rating2'):
                rating = form.cleaned_data.get('rating2')
            elif form.cleaned_data.get('rating3'):
                rating = form.cleaned_data.get('rating3')
            elif form.cleaned_data.get('rating4'):
                rating = form.cleaned_data.get('rating4')
            elif form.cleaned_data.get('rating5'):
                rating = form.cleaned_data.get('rating5')
            text = form.cleaned_data.get('text')
            parent = form.cleaned_data.get('parent')
            print(parent)
            parentComment = CommentModel.objects.filter(id=int(parent)).first()
            print(parentComment)
            newComment = CommentModel(text=text, book=product, rating=rating, user=request.user, parent=parentComment)
            newComment.save()
            return redirect(reverse('product-detail', args=[product.slug]))


class SearchPageView(View):
    def get(self, request: HttpRequest, name):
        items = ProductModel.objects.filter(name__contains=name).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        priceForm = PriceRangeForm()
        catgoryForm = CatgoryForm()
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page.html', {
            'page': page,
            'name': name,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, name):
        priceForm = PriceRangeForm(request.POST)
        catgoryForm = CatgoryForm(request.POST)

        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-price-filter', args=[name, start, end]))

        if catgoryForm.is_valid():
            catgory = catgoryForm.cleaned_data.get("catgory")
            return redirect(reverse('search-catgory-filter', args=[name, catgory]))

        return redirect(reverse('search', args=[name]))


class SearchPagePriceFileterView(View):
    def get(self, request: HttpRequest, name, start, end):
        print(name, start, end)
        items = ProductModel.objects.filter(name__contains=name, price__gt=start, price__lte=end).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        priceForm = PriceRangeForm()
        catgoryForm = CatgoryForm()
        filter = f'قیمت بین {start} و {end}'
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page.html', {
            'page': page,
            'name': name,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'filter': filter,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, name, start, end):
        priceForm = PriceRangeForm(request.POST)

        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-price-filter', args=[name, start, end]))


class SearchPageCatgoryFileterView(View):
    def get(self, request: HttpRequest, name, catgory):
        priceForm = PriceRangeForm()
        catgoryForm = CatgoryForm()
        catgoryObject = CatgoryModel.objects.filter(slug__contains=catgory).first()
        items = catgoryObject.productmodel_set.filter(name__contains=name).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        filter = catgoryObject.name
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page.html', {
            'page': page,
            'name': name,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'filter': filter,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, name, catgory):
        catgoryForm = CatgoryForm(request.POST)

        if catgoryForm.is_valid():
            catgoryObject = catgoryForm.cleaned_data.get('catgory')
            return redirect(reverse('search-catgory-filter', args=[name, catgoryObject]))


class SearchPageAllView(View):
    def get(self, request: HttpRequest):
        items = ProductModel.objects.filter(is_active=True).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        priceForm = PriceRangeForm()
        catgoryForm = CatgoryForm()
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page-all.html', {
            'page': page,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest):
        priceForm = PriceRangeForm(request.POST)
        catgoryForm = CatgoryForm(request.POST)

        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-all-price-filter', args=[start, end]))

        if catgoryForm.is_valid():
            catgory = catgoryForm.cleaned_data.get("catgory")
            return redirect(reverse('search-all-catgory-filter', args=[catgory]))


class SearchPageAllPriceFilterView(View):
    def get(self, request: HttpRequest, start, end):
        priceForm = PriceRangeForm(request.POST)
        catgoryForm = CatgoryForm(request.POST)
        items = ProductModel.objects.filter(price__gt=start, price__lte=end, is_active=True).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        filter = f'قیمت بین {start} و {end}'
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page-all.html', {
            'page': page,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'filter': filter,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, start, end):
        priceForm = PriceRangeForm(request.POST)

        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-all-price-filter', args=[start, end]))


class SearchPageAllCatgoryFilterView(View):
    def get(self, request: HttpRequest, catgory):
        priceForm = PriceRangeForm()
        catgoryForm = CatgoryForm()
        catgoryObject = CatgoryModel.objects.filter(slug__contains=catgory).first()
        items = catgoryObject.productmodel_set.filter(is_active=True).order_by('-price')
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        filter = catgoryObject.name
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page-all.html', {
            'page': page,
            'priceForm': priceForm,
            'catgoryForm': catgoryForm,
            'filter': filter,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, catgory):
        catgoryForm = CatgoryForm(request.POST)

        if catgoryForm.is_valid():
            catgoryobject = catgoryForm.cleaned_data.get("catgory")
            return redirect(reverse('search-all-catgory-filter', args=[catgoryobject]))


class SearchPageCatgoryView(View):
    def get(self, request: HttpRequest, catgory):
        catgoryObject = CatgoryModel.objects.filter(slug__contains=catgory).first()
        items = catgoryObject.productmodel_set.all()
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        priceForm = PriceRangeForm()
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page-catgory.html', {
            'page': page,
            'name': catgoryObject.name,
            'priceForm': priceForm,
            'slug': catgory,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, catgory):
        priceForm = PriceRangeForm(request.POST)
        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-catgory-price-filter', args=[catgory, start, end]))


class SearchPageCatgoryPriceFilterView(View):
    def get(self, request: HttpRequest, catgory, start, end):
        priceForm = PriceRangeForm()
        catgoryObject = CatgoryModel.objects.filter(slug__contains=catgory).first()
        items = catgoryObject.productmodel_set.filter(price__gt=start, price__lte=end)
        paginator = Paginator(items, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        filter = f'قیمت بین {start} و {end}'
        favoritProduct = []
        if request.user.is_authenticated:
            favorit = FavoriteProduct.objects.filter(user=request.user).all()
            for item in favorit:
                favoritProduct.append(item.product)
        return render(request, 'search-page-catgory.html', {
            'page': page,
            'name': catgoryObject.name,
            'priceForm': priceForm,
            'filter': filter,
            'slug': catgory,
            'favorit': favoritProduct
        })

    def post(self, request: HttpRequest, catgory, start, end):
        priceForm = PriceRangeForm(request.POST)
        if priceForm.is_valid():
            start = priceForm.cleaned_data.get('start')
            end = priceForm.cleaned_data.get('end')
            return redirect(reverse('search-catgory-price-filter', args=[catgory, start, end]))


def add_product_to_favorite(request):
    product_id = request.GET.get('id')
    product = ProductModel.objects.filter(id=product_id).first()
    if product is not None:
        favorite, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'status': 'add'})
        else:
            favorite.delete()
            return JsonResponse({'status': 'remove'})
    else:
        return JsonResponse({'status': 'Error'})


class ProductApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request:HttpRequest):
        data = ProductModel.objects.filter(is_active=True)
        query = ProductSerializer(data, many=True).data
        return Response(query)

    def post(self, request:HttpRequest):
        data = ProductSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
           data.save()
           return Response({'message': 'accept'})
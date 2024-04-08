from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import *

# Create your views here.
from django.views import View


class ProductDetailView(View):
    def get(self, request:HttpRequest, slug):
        product = ProductModel.objects.filter(slug=slug).first()
        comments = product.commentmodel_set.filter(parent=None)
        form = CommentForm()
        return render(request, 'product-detail.html', {
            'product' : product,
            'form' : form,
            'comments' : comments
        })

    def post(self, request:HttpRequest, slug):
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
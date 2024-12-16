from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class HeaderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'header.html')


class FooterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'footer.html')

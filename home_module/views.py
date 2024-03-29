from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeViews(View):
    def get(self, request):
        return render(request, 'home.html')

def headerView(request):
    return render(request, 'header.html')

def footerView(request):
    return render(request, 'footer.html')
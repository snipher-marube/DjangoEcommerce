from math import ceil

from django.shortcuts import render

from .models import Product

def home(request):
    user = request.user
    print(user)
    products = Product.objects.all()[0:3]
    context = {
        'products': products
    }
    return render(request, 'marketapp/home.html', context)

def contact(request):
    return render(request, 'marketapp/contact.html')
def cart(request):
    return render(request, 'marketapp/cart.html')

def checkout(request):
    return render(request, 'marketapp/checkout.html')

def shop(request):
    user = request.user
    print(user)
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'marketapp/shop-grid.html', context)


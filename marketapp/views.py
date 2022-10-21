from django.shortcuts import render

def home(request):
    return render(request, 'marketapp/home.html')

def contact(request):
    return render(request, 'marketapp/contact.html')
def cart(request):
    return render(request, 'marketapp/cart.html')

def checkout(request):
    return render(request, 'marketapp/checkout.html')

def shop(request):
    return render(request, 'marketapp/shop-grid.html')


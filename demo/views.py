from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from demo.forms import RegisterUserForm
from demo.models import *


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def about(request):
    products = Product.objects.filter(count__gte=1).order_by('-date')[:5]
    return render(request, 'demo/about.html', context={'products': products})


def catalog(request):
    products = Product.objects.filter(count__gte=1)
    return render(request, 'demo/catalog.html', context={'products': products})


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'demo/product.html', context={'product': product})


def contact(request):
    return render(request, 'demo/contact.html')


@login_required
def cart(request):
    return render(request, 'demo/cart.html')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'demo/orders.html', context={'orders': orders})

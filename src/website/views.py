from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from vendors.models import *
from .models import *


# Create your views here.


class HomeView(ListView):
    template_name = 'pages/index.html'
    queryset = Store.objects.all()
    context_object_name = 'shop_list'
    paginate_by = 4


class ProductDetailView(DetailView):
    template_name = 'pages/product_details.html'
    model = Product
    context_object_name = 'products'

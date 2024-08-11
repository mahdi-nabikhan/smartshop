from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from vendors.models import *


# Create your views here.


class HomeView(ListView):
    template_name = 'pages/index.html'
    queryset = Store.objects.all()
    context_object_name = 'shop_list'
    paginate_by = 4


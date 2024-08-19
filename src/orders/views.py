from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import *
from customers.models import *


# Create your views here.


class CustomerBill(View):
    def get(self, request, id):
        cart = Cart.objects.get(id=id)
        
        cart_item = OrderDetail.objects.filter(cart=cart)
        context = {'details': cart_item}
        return render(request, 'customer/bill.html', context)

    def post(self, request, id):
        pass

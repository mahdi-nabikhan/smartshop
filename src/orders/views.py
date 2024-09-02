from django.db.models import F, Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect

from .forms import AddressSelectionForm
from .models import *
from customers.models import *


# Create your views here.


# views.py


class CreateBillView(View):
    template_name = 'customer/bill.html'

    def get(self, request, id):

        form = AddressSelectionForm(user=request.user)
        cart = Cart.objects.get(id=id)
        orders = OrderDetail.objects.filter(cart=cart,  processed=False)
        cart2 = orders.annotate(result=F('product__price') * F('quantity'))
        cart23 = orders.annotate(result=F('product__price_after') * F('quantity'))
        total_price = cart2.aggregate(total_price=Sum('result'))['total_price']
        total_price_after_discount =cart23.aggregate(total_price=Sum('result'))['total_price']
        return render(request, self.template_name,
                      {'order_details': orders, 'form': form, 'total_price': total_price, 'cart': cart,'price_after_discount':total_price_after_discount}, )

    def post(self, request, id):
        form = AddressSelectionForm(request.POST, user=request.user)
        cart = Cart.objects.get(id=id)
        orders = OrderDetail.objects.filter(cart=cart)

        if form.is_valid():
            address = form.cleaned_data['address']

            bill = Bill.objects.create(cart=cart, address=address)

        return render(request, self.template_name, {'order_details': orders, 'form': form, 'cart': cart}, )


class PeyBill(View):
    template_name = 'customer/bill.html'

    def post(self, request, id):
        cart = Cart.objects.get(id=id)
        bill = Bill.objects.get(cart=cart)
        orders = OrderDetail.objects.filter(cart=cart, processed=False)

        orders.update(processed=True)
        cart.status=True
        cart.save()
        bill.status = True
        bill.save()

        return redirect('website:landing_page')

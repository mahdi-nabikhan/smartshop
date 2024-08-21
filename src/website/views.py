import http

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from vendors.models import *
from .models import *
from customers.models import Comments, Customer
from customers.forms import AddCommentForm
from orders.models import *
from .forms import *


# Create your views here.


class HomeView(ListView):
    template_name = 'pages/index.html'
    queryset = Store.objects.all()
    context_object_name = 'shop_list'
    paginate_by = 4


# class ProductDetailView(View):
#     template_name = 'pages/product_details.html'
#
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         comments = Comments.objects.filter(product=product)
#         add_comments = AddCommentForm()
#         context = {'products': product, 'comments': comments, 'add_comments': add_comments}
#
#         return render(request, self.template_name, context)
#
#     def post(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         customer = Customer.objects.get(pk=request.user.pk)
#         add_comments = AddCommentForm(request.POST)
#         if add_comments.is_valid():
#             add_comments.save(commit=False)
#             add_comments.instance.product = product
#             add_comments.instance.user = customer
#             add_comments.save()
#             return redirect('website:product_detail',pk=product.pk)
#         context = {'products': product, 'add_comments': add_comments}
#         return render(request, self.template_name, context)
class ProductDetailView(View):
    template_name = 'pages/product_details.html'

    def get(self, request, id):
        product = Product.objects.get(id=id)
        comments = Comments.objects.filter(product=product)
        form = QuantityForm()
        add_comment = AddCommentForm()
        can_rate=OrderDetail.objects.filter(product=product,cart__user=Customer.objects.get(id=request.user.id))
        total_rate = ProductRate.objects.filter(product=product).aggregate(total=Sum('rate'))['total'] / len(ProductRate.objects.filter(product=product))
        context = {'products': product, 'form': form, add_comment: 'add_comments', 'comments': comments, 'can_rate': can_rate,'total_rate':total_rate}
        return render(request, self.template_name, context)

    def post(self, request, id):
        form = QuantityForm(request.POST)
        add_comments = AddCommentForm(request.POST)
        customer = Customer.objects.get(pk=request.user.pk)
        product = Product.objects.get(id=id)
        comments = Comments.objects.filter(product=product)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product
            if request.user.is_authenticated:
                my_cart = Cart.objects.filter(user=request.user,status=False).first()
                if my_cart:

                    cart_item.cart = my_cart
                    cart_item.save()
                else:
                    customer=Customer.objects.get(id=request.user.id)
                    new=Cart.objects.create(user=customer)
                    cart_item.cart=new
                    cart_item.save()
            else:
                cart_items = request.session.get('cart_items', [])
                cart_items.append({
                    'product_id': product.id,
                    'quantity': cart_item.quantity
                })
                request.session['cart_items'] = cart_items

        if add_comments.is_valid():
            add_comments.save(commit=False)
            add_comments.instance.product = product
            add_comments.instance.user = customer
            add_comments.save()
            return redirect('website:product_detail', id=product.id)

        context = {'products': product, 'form': form, 'add_comments': add_comments, 'comments': comments}
        return render(request, self.template_name, context)


class AddProductRate(View):

    def get(self, request, id):
        customer = Customer.objects.get(id=request.user.id)
        order = OrderDetail.objects.filter(cart__user=customer)
        product = Product.objects.get(id=id)
        form = AddRatingForm()
        context = {
            'order': order,
            'product': product,
            'form': form
        }
        return render(request, 'customer/rate_products.html', context)

    def post(self, request, id):
        customer = Customer.objects.get(id=request.user.id)
        order = OrderDetail.objects.filter(cart__user=customer)
        product = Product.objects.get(id=id)
        form = AddRatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.product = product
            rate.save()
            return redirect('website:product_detail', id=product.id)
        context = {
            'order': order,
            'product': product,
            'form': form
        }
        return render(request, 'customer/rate_products.html', context)

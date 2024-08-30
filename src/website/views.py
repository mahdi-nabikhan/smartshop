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
        return render(request, 'pages/product_details.html', context)

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
            'form1': form
        }
        print('this is shit')
        return render(request, 'pages/product_details.html', context)


class ProductDetailView(View):
    template_name = 'pages/product_details.html'

    def get(self, request, id):
        product = Product.objects.get(id=id)
        comments = Comments.objects.filter(product=product)
        form = QuantityForm()
        add_comment = AddCommentForm()
        add_rating_form = AddRatingForm()

        can_rate = None

        if request.user.is_authenticated:
            can_rate = OrderDetail.objects.filter(product=product, cart__user=Customer.objects.get(id=request.user.id),
                                                  cart__status=True)
            print(can_rate)

        rate = ProductRate.objects.filter(product=product).exists()
        if rate:
            total_rate = ProductRate.objects.filter(product=product).aggregate(total=Sum('rate'))['total'] / len(
                ProductRate.objects.filter(product=product))
            context = {
                'products': product,
                'form': form,
                'add_comments': add_comment,
                'comments': comments,
                'total_rate': total_rate,
                'can_rate': can_rate,
                'add_rating_form': add_rating_form
            }
            return render(request, self.template_name, context)

        context = {
            'products': product,
            'form': form,
            'add_comments': add_comment,
            'comments': comments,
            'add_rating_form': add_rating_form
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        form = QuantityForm(request.POST)
        add_comments = AddCommentForm(request.POST)
        add_rating_form = AddRatingForm(request.POST)
        customer = Customer.objects.get(id=request.user.id)
        product = Product.objects.get(id=id)
        comments = Comments.objects.filter(product=product)

        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product

            new = Cart.objects.create(user=customer)
            cart_item.cart = new
            cart_item.save()

        if add_comments.is_valid():
            add_comments.save(commit=False)
            add_comments.instance.product = product
            add_comments.instance.user = customer
            add_comments.save()
            return redirect('website:product_detail', id=product.id)

        if add_rating_form.is_valid():
            rate = add_rating_form.save(commit=False)
            rate.product = product
            rate.save()
            return redirect('website:product_detail', id=product.id)

        context = {
            'products': product,
            'form': form,
            'add_comments': add_comments,
            'comments': comments,
            'add_rating_form': add_rating_form
        }
        return render(request, self.template_name, context)


class Search(ListView):
    model = Product
    template_name = 'customer/search_products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        product_name = self.request.GET.get('q')
        all_products = self.get_queryset().filter(name__icontains=product_name)
        context["products"] = all_products
        context["not_found"] = f'{product_name} does not exist.'
        return context


class SearchStore(ListView):
    model = Store
    template_name = 'pages/index.html'
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        context = super(SearchStore, self).get_context_data(**kwargs)
        store_name = self.request.GET.get('q')

        all_store = self.get_queryset().filter(name__icontains=store_name)
        products = Product.objects.filter(name__icontains=store_name)
        context["shop_list"] = all_store
        context["products"] = products
        context["not_found"] = f'{store_name} does not exist.'
        return context


class TopRatedStoresView(ListView):
    template_name = 'pages/top_rated_stores.html'
    context_object_name = 'shop_list'
    paginate_by = 4

    def get_queryset(self):
        print(Store.objects.annotate(total_rate=Sum('store_rate__rate')).order_by('-total_rate'))
        return Store.objects.annotate(total_rate=Sum('store_rate__rate')).order_by('-total_rate')


from django.db.models import Count


class TopSellingStoresView(ListView):
    model = Store
    template_name = 'pages/top_selling_stores.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        processed_orders = OrderDetail.objects.filter(processed=True)

        store_sales = processed_orders.values('product__store').annotate(total_sales=Count('id')).order_by(
            '-total_sales')

        top_stores = Store.objects.filter(id__in=[store['product__store'] for store in store_sales])

        return top_stores


class ShopList(ListView):
    template_name = 'pages/shop_list.html'
    queryset = Store.objects.all()
    context_object_name = 'shop_list'
    paginate_by = 5

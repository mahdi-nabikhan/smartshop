from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from vendors.models import *
from .models import *
from customers.models import Comments, Customer
from customers.forms import AddCommentForm


# Create your views here.


class HomeView(ListView):
    template_name = 'pages/index.html'
    queryset = Store.objects.all()
    context_object_name = 'shop_list'
    paginate_by = 4


class ProductDetailView(View):
    template_name = 'pages/product_details.html'

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        comments = Comments.objects.filter(product=product)
        add_comments = AddCommentForm()
        context = {'products': product, 'comments': comments, 'add_comments': add_comments}

        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(pk=request.user.pk)
        add_comments = AddCommentForm(request.POST)
        if add_comments.is_valid():
            add_comments.save(commit=False)
            add_comments.instance.product = product
            add_comments.instance.user = customer
            add_comments.save()
            return redirect('website:product_detail',pk=product.pk)
        context = {'products': product, 'add_comments': add_comments}
        return render(request, self.template_name, context)

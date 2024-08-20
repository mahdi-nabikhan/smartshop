from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView, TemplateView, ListView
from django.urls import reverse_lazy
from .models import Store
from website.models import *
from .forms import *
from .permissions import *
from django.utils.decorators import method_decorator
from orders.models import *

from django.db.models import F
from django.shortcuts import render
from django.views import View


# Create your views here.


class RegisterStores(View):
    template_name = 'admins/owner_register.html'

    def get(self, request):
        form = RegistrationManagerForms()
        store_form = RegistrationStoreForm()
        address_form = AddressStoreForm()
        context = {'form': form, 'store_form': store_form, 'address_form': address_form}
        return render(request, 'admins/owner_register.html', context)

    def post(self, request):
        form = RegistrationManagerForms(request.POST)
        store_form = RegistrationStoreForm(request.POST, request.FILES)
        address_form = AddressStoreForm(request.POST)
        if form.is_valid() and address_form.is_valid() and store_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            store = store_form.save(commit=False)
            store.owner = user
            store.save()
            address = address_form.save(commit=False)
            address.store = store
            address.save()
            return redirect('website:landing_page')
        context = {'form': form, 'store_form': store_form, 'address_form': address_form}
        return render(request, 'admins/owner_register.html', context)


# class RegisterStoreView(View):
#
#     def get(self, request, id):
#         form = RegistrationStoreForm()
#         context = {'form': form}
#         return render(request, 'store_register.html', context)
#
#     def post(self, request, id):
#         form = RegistrationStoreForm(request.POST)
#         user = User.objects.get(id=id)
#         if form.is_valid():
#             store = form.save(commit=False)
#             store.owner = user
#             store.save()
#             return redirect('vendors:add_address_store', id=store.id)
#         context = {'form': form}
#         return render(request, 'store_register.html', context)
#
#
# class StoreAddressView(View):
#     def get(self, request, id):
#         form = AddressStoreForm()
#         context = {'form': form}
#         return render(request, 'storeaddress.html', context)
#
#     def post(self, request, id):
#         stores_obj = Store.objects.get(id=id)
#         print(stores_obj)
#         form = AddressStoreForm(request.POST)
#         if form.is_valid():
#             stores = form.save(commit=False)
#             stores.store = stores_obj
#             stores.save()
#             return redirect('website:landing_page')
#         return render(request, 'storeaddress.html', {'form': form})

@method_decorator(is_manager, name='dispatch')
class AdminRegisterStore(View):

    def get(self, request, id):
        form = AdminRegisterForm()
        context = {'form': form}
        return render(request, 'admins/admin_register.html', context)

    def post(self, request, id):
        store = Store.objects.get(id=id)
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.set_password(form.cleaned_data['password'])
            admin.store = store
            admin.save()
            return redirect('dashboards:admin_panel')
        context = {'form': form}
        return render(request, 'admins/admin_register.html', context)


@method_decorator(admin_or_manager_required, name='dispatch')
class AddProductView(View):
    template_name = 'admins/add_product.html'

    def get(self, request, id):
        form = AddProductForm()
        discount_form = AddDiscountForm()
        context = {'form': form, 'discount_form': discount_form}
        return render(request, 'admins/add_product.html', context)

    def post(self, request, id):
        form = AddProductForm(request.POST, request.FILES)
        store = Store.objects.get(id=id)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            ProductImages.objects.create(product=product, product_image=form.cleaned_data['image'])
            return redirect('dashboards:admin_panel')
        context = {'form': form}
        return render(request, 'admins/add_product.html', context)


class ProductListView(View):

    def get(self, request, id):
        store = Store.objects.get(id=id)
        products = Product.objects.filter(store=store)
        context = {'products': products}
        return render(request, 'admins/product_list.html', context)


class ProductDetailView(DetailView):
    template_name = 'admins/product_detail.html'
    model = Product
    context_object_name = 'products'


@method_decorator(admin_or_manager_required, name='dispatch')
class DeleteImageView(DeleteView):
    template_name = 'admins/image_delete.html'
    model = ProductImages
    success_url = reverse_lazy('dashboards:admin_panel')


@method_decorator(admin_or_manager_required, name='dispatch')
class AddImageView(View):

    def get(self, request, id):
        form = AddImageForm()
        context = {'form': form}
        return render(request, 'admins/add_image.html', context)

    def post(self, request, id):
        form = AddImageForm(request.POST, request.FILES)
        product = Product.objects.get(id=id)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            return redirect('dashboards:admin_panel')
        context = {'form': form}
        return render(request, 'admins/add_image.html', context)


@method_decorator(admin_or_manager_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = 'admins/add_product.html'
    success_url = reverse_lazy('dashboards:admin_panel')


@method_decorator(is_manager, name='dispatch')
class UpdateStoreView(UpdateView):
    model = Store
    form_class = UpdateStoreForm
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/update_store.html'


@method_decorator(is_manager, name='dispatch')
class UpdateManager(UpdateView):
    model = Managers
    form_class = UpdateManagersForm
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/update_managers.html'


class StoreDetail(DetailView):
    template_name = 'pages/single.html'
    model = Store
    context_object_name = 'store'

    def get_context_data(self, **kwargs):
        store = self.get_object()
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(store=store)
        paginator = Paginator(products, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        context['address'] = StoreAddress.objects.filter(store=store)
        return context


@method_decorator(admin_or_manager_required, name='dispatch')
class UpdateDiscount(UpdateView):
    model = Discount
    form_class = AddDiscountForm
    context_object_name = 'form'
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/update_discount.html'


@method_decorator(admin_or_manager_required, name='dispatch')
class AddDiscountView(View):
    def get(self, request, id):
        form = AddDiscountForm()
        context = {'form': form}
        return render(request, 'admins/add_discount.html', context)

    def post(self, request, id):
        form = AddDiscountForm(request.POST)
        product = Product.objects.get(id=id)

        if form.is_valid():
            discount = form.save()
            product.discount = discount
            if product.discount:
                if product.discount.discount_type == 'cash':
                    product.price_after = product.price - product.discount.value
                    product.save()
                    return redirect('dashboards:admin_panel')
                elif product.discount.discount_type == 'percentage':
                    product.price_after = max(0, product.price - (product.price * (product.discount.value // 100)))
                    product.save()
                    return redirect('dashboards:admin_panel')
                else:
                    product.save()
                    return redirect('dashboards:admin_panel')
        return render(request, '', {'form': form})


@method_decorator(admin_or_manager_required, name='dispatch')
class DeleteDiscountView(DeleteView):
    model = Discount
    context_object_name = 'discount'
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/delete_discount.html'


class RegisterOperator(View):

    def get(self, request, id):
        form = RegisterOperators()
        context = {'form': form}
        return render(request, 'admins/operator_register.html', context)

    def post(self, request, id):
        store = Store.objects.get(id=id)
        form = RegisterOperators(request.POST)
        if form.is_valid():
            operator = form.save(commit=False)
            operator.set_password(form.cleaned_data['password'])
            operator.store = store
            operator.save()
            return redirect('dashboards:admin_panel')
        context = {'form': form}
        return render(request, 'admins/operator_register.html', context)


@method_decorator(is_manager, name='dispatch')
class AdminListView(View):
    def get(self, request, id):
        store = Store.objects.get(id=id)
        admin = Admin.objects.filter(store=store)
        context = {'admin': admin}
        return render(request, 'admins/admin_list.html', context)


@method_decorator(is_manager, name='dispatch')
class DeleteAdminView(DeleteView):
    model = Admin
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/delete_discount.html'


@method_decorator(is_manager, name='dispatch')
class OperatorListView(View):
    def get(self, request, id):
        store = Store.objects.get(id=id)
        admin = Operator.objects.filter(store=store)
        context = {'admin': admin}
        return render(request, 'admins/admin_list.html', context)


@method_decorator(is_manager, name='dispatch')
class DeleteOperatorView(DeleteView):
    model = Operator
    success_url = reverse_lazy('dashboards:admin_panel')
    template_name = 'admins/delete_discount.html'


# views.py

class ListOrderDetails(View):
    def get(self, request, id):
        store = Store.objects.get(id=id)
        orders = OrderDetail.objects.filter(product__store=store)
        context = {
            'orders': orders
        }
        return render(request, 'admins/order_details.html', context)


# urls.py


class DetailOrderDetails(View):
    template_name = 'admins/order_detail_2.html'

    def get(self, request, pk):
        order_detail = OrderDetail.objects.filter(pk=pk).annotate(result=F('product__price') * F('quantity')).first()
        context = {'order_detail': order_detail, 'total': order_detail.result if order_detail else 0}
        return render(request, 'admins/order_detail_2.html', context)


class OrderDetailUpdated(UpdateView):
    model = OrderDetail
    form_class = OrderDetailForm
    success_url = reverse_lazy('dashboards:admin_panel')
    context_object_name = 'forms'
    template_name = 'admins/order_update.html'

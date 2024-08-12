from django.shortcuts import render, redirect
from django.views import View
from .models import Store

from .forms import RegistrationStoreForm, AddressStoreForm, RegistrationManagerForms, AdminRegisterForm


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

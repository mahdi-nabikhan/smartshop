from django.shortcuts import render,redirect
from django.views import View
from .models import Store
from accounts.models import User
from customers.forms import RegisterForm
from .forms import RegistrationStoreForm, AddressStoreForm


# Create your views here.


class RegisterManager(View):
    template_name = 'owner_register.html'

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'owner_register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'manager'
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('vendors:store_register',id=user.id)
        context = {'form': form}
        return render(request, 'owner_register.html', context)


class RegisterStoreView(View):

    def get(self, request, id):
        form = RegistrationStoreForm()
        context = {'form': form}
        return render(request, 'store_register.html', context)

    def post(self, request, id):
        form = RegistrationStoreForm(request.POST)
        user = User.objects.get(id=id)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = user
            store.save()
            return redirect('vendors:add_address_store',id=store.id)
        context = {'form': form}
        return render(request, 'store_register.html', context)


class StoreAddressView(View):
    def get(self, request, id):
        form = AddressStoreForm()
        context = {'form': form}
        return render(request,'storeaddress.html',context)

    def post(self, request, id):
        stores_obj = Store.objects.get(id=id)
        print(stores_obj)
        form = AddressStoreForm(request.POST)
        if form.is_valid():
            stores = form.save(commit=False)
            stores.store = stores_obj
            stores.save()
            return redirect('website:landing_page')
        return render(request, 'storeaddress.html', {'form': form})

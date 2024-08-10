from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView
from .models import *
from .forms import RegisterForm, AddressForm


# Create your views here.
class CustomerRegisterView(View):
    template_name = 'customer/register.html'

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('customers:add_address', id=user.id)
        return render(request, 'customer/register.html', {'form': form})


class AddAddressView(View):
    template_name = 'customer/address.html'

    def get(self, request, id):
        form = AddressForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, id):
        user = Customer.objects.get(id=id)
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            return redirect('website:landing_page')
        return render(request, 'customer/address.html', {'form': form})


class ProfileCustomer(DetailView):
    template_name = 'customer/profile.html'
    model = User
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['addresses'] = Address.objects.filter(user=user)
        return context


class UpdateCustomer(UpdateView):
    template_name = 'customer/customer_edit_profile.html'
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    success_url = reverse_lazy('website:landing_page')

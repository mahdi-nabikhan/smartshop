from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User
from .forms import RegisterForm,AddressForm


# Create your views here.
class CustomerRegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'customer'
            user.save()
            return redirect('accounts:add_address', id=user.id)
        return render(request, 'register.html', {'form': form})


class AddAddressView(View):
    template_name = 'address.html'

    def get(self, request, id):
        form = AddressForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            return redirect('accounts:index')
        return render(request, self.template_name, {'form': form})

from django.shortcuts import render
from django.views import View
from customers.forms import RegisterForm


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
        context = {'form': form}
        return render(request, 'owner_register.html', context)

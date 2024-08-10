from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from vendors.models import *
from accounts.forms import LoginForm


# Create your views here.
class LoginViews(View):
    template_name = 'customer/login.html'

    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if Managers.objects.filter(pk=user.pk):
                    return redirect('dashboards:admin_panel')
                else:
                    return redirect('website:landing_page')
        return render(request, self.template_name, {'form': form})


def logoutview(request):
    logout(request)
    return redirect('website:landing_page')

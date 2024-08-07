from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


# Create your views here.
class LoginViews(LoginView):
    template_name = 'login.html'

    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.role == 'manager' or user.role == 'admin':
            return redirect('accounts:manager', pk=user.manager.id)
        return redirect(self.success_url)

from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import FormView

from accounts.forms import LoginForm
from customers.models import Customer
from vendors.models import *
from .forms import PhoneNumberForm
from .forms import VerificationCodeForm
from .models import VerificationCode, User


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

                if Managers.objects.filter(id=user.id).exists() or Admin.objects.filter(
                        id=user.id).exists() or Operator.objects.filter(id=user.id).exists():
                    return redirect('dashboards:admin_panel')

                elif Customer.objects.filter(id=user.id):
                    return redirect('website:landing_page')

        return render(request, self.template_name, {'form': form})


def logoutview(request):
    logout(request)
    return redirect('website:landing_page')


class SendVerificationCodeView(FormView):
    template_name = 'send_code.html'
    form_class = PhoneNumberForm

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        user = get_object_or_404(User, phone=phone_number)
        verification_code = VerificationCode(user=user)
        verification_code.save()
        print(f"Verification code for {user.phone}: {verification_code.code}")
        return redirect('accounts:verify_code', phone_number=phone_number)


class VerifyCodeView(View):
    def get(self, request, phone_number):
        form = VerificationCodeForm()
        return render(request, 'verify_code.html', {'form': form, 'phone_number': phone_number})

    def post(self, request, phone_number):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = get_object_or_404(User, phone=phone_number)
            verification_code = get_object_or_404(VerificationCode, user=user, code=code)

            if verification_code:
                login(request, user)
                if Managers.objects.filter(id=user.id).exists() or Admin.objects.filter(
                        id=user.id).exists() or Operator.objects.filter(id=user.id).exists():
                    return redirect('dashboards:admin_panel')

                return redirect('website:landing_page')
            else:
                return HttpResponse("wrong pass word.")
        return render(request, 'verify_code.html', {'form': form, 'phone_number': phone_number})

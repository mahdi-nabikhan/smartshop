from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, FormView
from .models import *
from .forms import RegisterForm, AddressForm, AddCommentForm
from website.forms import AddRatingForm
from orders.models import *
from accounts.models import *
from accounts.forms import *


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
    model = Customer
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['addresses'] = Address.objects.filter(user=user)
        context['comment'] = Comments.objects.filter(user=user)
        context['bill'] = Bill.objects.filter(cart__user=user)
        return context


class UpdateCustomer(UpdateView):
    template_name = 'customer/customer_edit_profile.html'
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    success_url = reverse_lazy('website:landing_page')


class UpdateAddress(UpdateView):
    model = Address
    template_name = 'customer/address_edit.html'
    form_class = AddressForm
    success_url = reverse_lazy('website:landing_page')
    context_object_name = 'form'


class SeeOrderDetail(ListView):
    queryset = OrderDetail.objects.filter(status='P')
    template_name = 'customer/order_detail_status_pendding.html'
    context_object_name = 'orders'


class SeeOrderDetailRejected(ListView):
    queryset = OrderDetail.objects.filter(status='C')
    template_name = 'customer/order_detail_status_rejected.html'
    context_object_name = 'orders'


class SeeOrderDetailComformed(ListView):
    queryset = OrderDetail.objects.filter(status='C')
    template_name = 'customer/order_derail_status_comfied.html'
    context_object_name = 'orders'


class OrderDetailDetailView(View):
    template_name = 'customer/seeorderdetails.html'

    def get(self, request, pk):
        orders = OrderDetail.objects.get(pk=pk)
        form = AddRatingForm()
        add_comment = AddCommentForm()
        context = {'orders': orders, 'form': form, 'add_comment': add_comment}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        orders = OrderDetail.objects.get(pk=pk)
        form = AddRatingForm(request.POST)
        add_comment = AddCommentForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = orders.product
            rating.save()
        if add_comment.is_valid():
            comment = add_comment.save(commit=False)
            comment.product = orders.product
            comment.user = Customer.objects.get(id=request.user.id)
            comment.save()

        context = {'orders': orders, 'form': form, 'add_comment': add_comment}
        return render(request, template_name=self.template_name, context=context)


class CartDetails(View):
    def get(self, request, id):
        cart = Cart.objects.get(id=id, status=True)
        print(cart)
        order = OrderDetail.objects.filter(cart=cart)

        print(order)
        cart2 = order.annotate(result=F('product__price') * F('quantity'))
        total_price = cart2.aggregate(total_price=Sum('result'))['total_price']
        context = {'orders': order, 'total_price': total_price}
        print(context)
        return render(request, 'customer/cart_details.html', context)


class SendVerificationCodeView(FormView):
    template_name = 'customer/send_code2.html'
    form_class = PhoneNumberForm

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        user = get_object_or_404(User, phone=phone_number)
        verification_code = VerificationCode(user=user)
        verification_code.save()
        print(f"Verification code for {user.phone}: {verification_code.code}")
        return redirect('customers:verify_code', phone_number=phone_number)


class VerifyCodeView(View):
    def get(self, request, phone_number):
        form = VerificationCodeForm()
        return render(request, 'customer/verify_code2.html', {'form': form, 'phone_number': phone_number})

    def post(self, request, phone_number):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = get_object_or_404(User, phone=phone_number)
            verification_code = get_object_or_404(VerificationCode, user=user, code=code)

            if verification_code:
                return redirect('customers:password_change')

            else:
                return HttpResponse('hi')
        return render(request, 'verify_code.html', {'form': form, 'phone_number': phone_number})




class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'customer/password_change.html'
    success_url = reverse_lazy('website:landing_page')

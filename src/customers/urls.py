from django.urls import path

from customers.views import CustomerRegisterView, AddAddressView, ProfileCustomer

app_name = 'customers'
urlpatterns = [
    path('customer_register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('add_adress/<int:id>', AddAddressView.as_view(), name='add_address'),
    path('customer_profile/<int:id>',ProfileCustomer.as_view(), name='customer_profile'),


]

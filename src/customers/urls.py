from django.urls import path

from customers.views import CustomerRegisterView, AddAddressView, ProfileCustomer,UpdateCustomer

app_name = 'customers'
urlpatterns = [
    path('customer_register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('add_adress/<int:id>', AddAddressView.as_view(), name='add_address'),
    path('customer_profile/<int:pk>',ProfileCustomer.as_view(), name='customer_profile'),
    path('customer_edit_info/<int:pk>',UpdateCustomer.as_view(), name='customer_edit_info'),




]

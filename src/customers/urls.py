from django.urls import path

from customers.views import *
app_name = 'customers'
urlpatterns = [
    path('customer_register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('add_adress/<int:id>', AddAddressView.as_view(), name='add_address'),
    path('customer_profile/<int:pk>',ProfileCustomer.as_view(), name='customer_profile'),
    path('customer_edit_info/<int:pk>',UpdateCustomer.as_view(), name='customer_edit_info'),
    path('edit_address/<int:pk>',UpdateAddress.as_view(), name='edit_address'),
    path('order_detail/',SeeOrderDetail.as_view(),name = 'order_details'),
    path('order_detail/rejected/',SeeOrderDetailRejected.as_view(),name = 'order_details_rejected'),
    path('order_detail/comfied/',SeeOrderDetailComformed.as_view(),name = 'order_details_comfied'),
    path('order_details/<int:pk>/',OrderDetailDetailView.as_view(),name='detail_detail'),
    path('cart_details/<int:id>/',CartDetails.as_view(),name='cart_detail'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('phone_login/', SendVerificationCodeView.as_view(), name='phone'),
    path('verify_code/<str:phone_number>/', VerifyCodeView.as_view(), name='verify_code')
]


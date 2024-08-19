from django.urls import path,include
from .views import CustomerBill
app_name = 'orders'
urlpatterns = [
    path('',include('orders.api.urls'),name='api_urls'),
    path('bill/<int:id>/',CustomerBill.as_view(),name='customer_bill')
]
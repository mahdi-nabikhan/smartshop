from django.urls import path,include
from .views import CreateBillView,PeyBill
app_name = 'orders'
urlpatterns = [
    path('',include('orders.api.urls'),name='api_urls'),
    path('bill/<int:id>/',CreateBillView.as_view(),name='customer_bill'),
    path('pay_bill/<int:id>/',PeyBill.as_view(),name='pay_bill'),
]
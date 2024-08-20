from django.urls import path,include
from .views import CreateBillView
app_name = 'orders'
urlpatterns = [
    path('',include('orders.api.urls'),name='api_urls'),
    path('bill/<int:id>/',CreateBillView.as_view(),name='customer_bill')
]
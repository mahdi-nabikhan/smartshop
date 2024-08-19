from django.urls import path,include

app_name = 'orders'
urlpatterns = [
    path('',include('orders.api.urls'),name='api_urls')
]
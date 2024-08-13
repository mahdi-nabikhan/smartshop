from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='landing_page'),
    path('product_detail/<int:pk>/',ProductDetailView.as_view(),name='product_detail')
]
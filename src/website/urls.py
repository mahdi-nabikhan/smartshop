from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='landing_page'),
    path('product_detail/<int:id>/',ProductDetailView.as_view(),name='product_detail'),
    path('product_rate/<int:id>/',AddProductRate.as_view(),name='product_rate'),

]
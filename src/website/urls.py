from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='landing_page'),
    path('product_detail/<int:id>/',ProductDetailView.as_view(),name='product_detail'),
    path('product_rate/<int:id>/',AddProductRate.as_view(),name='product_rate'),
    path('search_products/',Search.as_view(),name='search_products'),
    path('store_search/',SearchStore.as_view(),name='store_search'),
    path('top_rate_store/',TopRatedStoresView.as_view(),name='top_rate_store'),
path('top-selling-stores/', TopSellingStoresView.as_view(), name='top_selling_stores')

]
from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='landing_page'),
    path('product_detail/<int:id>/',ProductDetailView.as_view(),name='product_detail'),
    path('product_rate/<int:id>/',AddProductRate.as_view(),name='product_rate'),
    path('search_products/',Search.as_view(),name='search_products'),
    path('store_search/',SearchStore.as_view(),name='store_search'),
    path('top-rated-and-selling-stores/', TopRatedAndSellingStoresView.as_view(), name='top_rated_and_selling_stores'),
    path('all_shops/',ShopList.as_view(),name='all_shops'),

]
from django.urls import path
from .views import *

app_name = 'vendors'
urlpatterns = [
    path('manager_register/', RegisterStores.as_view(), name='manager_register'),
    path('admin_register/<int:id>/', AdminRegisterStore.as_view(), name='admin_register'),
    path('add_product/<int:id>/', AddProductView.as_view(), name='add_product'),
    path('product_list/<int:id>/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('delete_image/<int:pk>/', DeleteImageView.as_view(), name='delete_image'),
    path('add_image/<int:id>/', AddImageView.as_view(), name='add_image'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('update_store/<int:pk>/', UpdateStoreView.as_view(), name='update_store'),
    path('update_manager/<int:pk>/', UpdateManager.as_view(), name='update_manager'),
    path('store_detail/<int:pk>/', StoreDetail.as_view(), name='store_detail'),
    path('add_discounts/', AddDiscountView.as_view(), name='add_discount'),
    path('update_discount/<int:pk>/', UpdateDiscount.as_view(), name='update_discounts'),
    path('delete_discount/<int:pk>/', DeleteDiscountView.as_view(), name='delete_discount'),
    path('operator_register/<int:id>/', RegisterOperator.as_view(), name='operator_register'),

    # path('store_register/<int:id>',RegisterStoreView.as_view(),name='store_register'),
    # path('add_address_store/<int:id>',StoreAddressView.as_view(),name='add_address_store'),

]

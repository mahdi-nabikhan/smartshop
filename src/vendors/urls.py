from django.urls import path
from .views import *
app_name = 'vendors'
urlpatterns = [
    path('manager_register/',RegisterManager.as_view(),name='manager_register'),
    path('store_register/<int:id>',RegisterStoreView.as_view(),name='store_register'),
    path('add_address_store/<int:id>',StoreAddressView.as_view(),name='add_address_store'),

]
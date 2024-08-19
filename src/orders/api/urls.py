from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
app_name='api'
urlpatterns = [
    path('api/cart-items/', CartItemAPIView.as_view(), name='cart_items_api'),
    path('finalize-cart/', finalize_cart, name='finalize_cart'),
    path('cart-items/', cart_items_view, name='cart_items_view'),
    path('is-authenticated/', is_authenticated, name='is_authenticated'),
    path('not-authenticated/', not_authenticated, name='not_authenticated'),
    path('cart-items/<int:id>/', CartItemAPIView.as_view(), name='cart_item_detail_api'),
    path('login/', auth_views.LoginView.as_view(template_name='customer/login.html'), name='login'),
]

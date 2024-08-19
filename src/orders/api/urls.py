from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
app_name = 'cart'
from accounts . views import *
router = DefaultRouter()
router.register('product', ProductAPIView, basename='product')
router.register('cart', CartViewSet, basename='cart')
router.register('cartitem', CartItemView, basename='CartItem')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cart-items/', CartItemAPIView.as_view(), name='cart-items-api'),
    path('api/cart-items/<int:id>/', CartItemAPIView.as_view(),name='cart-item-detail'),
    path('cart1/', cart_items_view, name='cart-items-view'),
    path('product_list/',ProductListView.as_view(), name='product_list'),
    # path('product_list/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/is-authenticated/', is_authenticated, name='is_authenticated'),
    path('api/not-authenticated/', not_authenticated, name='not_authenticated'),
    path('finalize-cart/', finalize_cart, name='finalize_cart'),
    path('login/',LoginViews.as_view(), name='login'),
]

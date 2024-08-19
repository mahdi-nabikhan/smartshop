from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.viewsets import *
from .serializers import *
from orders.models import *



# Create your views here.

# class ProductAPIView(APIView):
#     serializer_class = ProductSerializer
#
#     def get(self, request):
#         product = Products.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
# class ProductAPIView(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Products.objects.all()

class ProductAPIView(ViewSet):
    serializer_class = ProductSerializer

    def list(self, request):
        product = Products.objects.all()
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            serializer = self.serializer_class(product)
            return Response(serializer.data)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetailAPIView(APIView):
#     serializer_class = ProductSerializer
#
#     def get_object(self, pk):
#         product = Products.objects.get(pk=pk)
#         return product
#
#     def get(self, request, pk):
#         product = Products.objects.get(pk=pk)
#         serializer = self.serializer_class(product)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = Products.objects.get(pk=pk)
#         serializer = self.serializer_class(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = Products.objects.get(pk=pk)
#         product.delete()
#
#     def patch(self, request, pk):
#         product = Products.objects.get(pk=pk)
#         serializer = self.serializer_class(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
# class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Products.objects.all()
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk, user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk, user=request.user)
            serializer = CartSerializer(cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk, user=request.user)
            serializer = CartSerializer(cart, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk, user=request.user)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)


# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import Cart, CartItem, Products
# from .serializers import CartItemSerializer
#
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Cart, CartItem, Products
# from .serializers import CartItemSerializer
#
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Cart, CartItem, Products
# from .serializers import CartItemSerializer


class CartItemView(viewsets.ViewSet):

    def list(self, request):
        cart = Cart.objects.get(user=request.user)
        items = OrderDetail.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        cart = Cart.objects.get(user=request.user)
        product = Products.objects.get(id=request.data['product_id'])
        cart_item = OrderDetail.objects.create(cart=cart, product=product)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        cart_item = OrderDetail.objects.get(pk=pk)
        cart_item.product = Products.objects.get(id=request.data['product_id'])
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        cart_item = OrderDetail.objects.get(pk=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemListView(APIView):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = OrderDetail.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .models import CartItem
# from .serializers import CartItemSerializer

# class CartItemAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         cart_items = CartItem.objects.filter(cart__user=request.user)
#         serializer = CartItemSerializer(cart_items, many=True)
#         return Response(serializer.data)
#
#     def delete(self, request, id):
#         try:
#             cart_item = CartItem.objects.get(id=id, cart__user=request.user)
#             cart_item.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
# class CartItemAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         cart_items = CartItem.objects.filter(cart__user=request.user)
#         serializer = CartItemSerializer(cart_items, many=True)
#         return Response(serializer.data)
#
#     def delete(self, request, id):
#         try:
#             cart_item = CartItem.objects.get(id=id, cart__user=request.user)
#             cart_item.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

# def patch(self, request, id):
#
#     try:
#         cart_item = CartItem.objects.get(id=id)
#         serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             print(request.data)
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except CartItem.DoesNotExist:
#         return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import CartItem
# from .serializers import CartItemSerializer
# from rest_framework.permissions import IsAuthenticated
#
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import CartItem, Products, Cart
# from .serializers import CartItemSerializer


class CartItemAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = OrderDetail.objects.filter(cart__user=request.user)
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        else:
            cart_items = request.session.get('cart_items', [])
            return Response(cart_items)

    def delete(self, request, id):
        if request.user.is_authenticated:
            try:
                cart_item = OrderDetail.objects.get(id=id, cart__user=request.user)
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except OrderDetail.DoesNotExist:
                return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart_items = request.session.get('cart_items', [])
            cart_items = [item for item in cart_items if item['id'] != id]
            request.session['cart_items'] = cart_items
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        if request.user.is_authenticated:
            try:
                cart_item = OrderDetail.objects.get(id=id, cart__user=request.user)
                serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except OrderDetail.DoesNotExist:
                return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart_items = request.session.get('cart_items', [])
            for item in cart_items:
                if item['id'] == id:
                    item.update(request.data)
            request.session['cart_items'] = cart_items
            return Response(status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            product = Products.objects.get(id=request.data['product_id'])
            cart_item = OrderDetail.objects.create(cart=cart, product=product, quantity=request.data['quantity'])
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart_items = request.session.get('cart_items', [])
            cart_items.append({
                'id': len(cart_items) + 1,
                'product_id': request.data['product_id'],
                'quantity': request.data['quantity']
            })
            request.session['cart_items'] = cart_items
            return Response(status=status.HTTP_201_CREATED)


@login_required
def finalize_cart(request):
    cart_items = request.session.get('cart_items', [])
    if cart_items:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        for item in cart_items:
            product = Products.objects.get(id=item['product_id'])
            OrderDetail.objects.create(cart=cart, product=product, quantity=item['quantity'])
        del request.session['cart_items']
    return redirect('cart:cart-items-view')


from django.shortcuts import render
from .models import Products


def cart_items_view(request):
    if request.user.is_authenticated:
        return render(request, 'cart_items.html')
    else:
        cart_items = request.session.get('cart_items', [])

        cart_items = [
            {
                'product': Products.objects.get(id=item['product_id']),
                'quantity': item['quantity']
            }
            for item in cart_items
        ]
        context = {'cart_items': cart_items}
        return render(request, 'cart_items.html', context)


class ProductListView(ListView):
    model = Products
    template_name = 'product_list.html'
    context_object_name = 'products'


# from .forms import *
#
#
# class ProductDetailView(View):
#     template_name = 'product_detail.html'
#
#     def get(self, request, id):
#         product = Products.objects.get(id=id)
#         form = QuantityForm()
#         context = {'product': product, 'form': form}
#         return render(request, self.template_name, context)
#
#     def post(self, request, id):
#         form = QuantityForm(request.POST)
#         product = Products.objects.get(id=id)
#         if form.is_valid():
#             cart_item = form.save(commit=False)
#             cart_item.product = product
#             if request.user.is_authenticated:
#                 cart = Cart.objects.filter(user=request.user).first()
#                 if not cart:
#                     cart = Cart.objects.create(user=request.user)
#                 cart_item.cart = cart
#                 cart_item.save()
#             else:
#                 cart_items = request.session.get('cart_items', [])
#                 cart_items.append({
#                     'product_id': product.id,
#                     'quantity': cart_item.quantity
#                 })
#                 request.session['cart_items'] = cart_items
#         context = {'product': product, 'form': form}
#         return render(request, self.template_name, context)


# class IsUserAuth(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return True
#         return render(request, 'cart_items.html',{'user':request.user})
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def is_authenticated(request):
    return JsonResponse({'is_authenticated': True})

def not_authenticated(request):
    return JsonResponse({'is_authenticated': False})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from website.models import Product
from customers.models import *
from orders.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .serializers import CartItemSerializer, CartItemSerializer2


class CartItemAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(id=request.user.id)

            cart_items = OrderDetail.objects.filter(cart__user=customer, processed=False)
            serializer = CartItemSerializer2(cart_items, many=True)
            return Response(serializer.data)
        else:
            cart_items = request.session.get('cart_items', [])
            return Response(cart_items)

    def delete(self, request, id):
        if request.user.is_authenticated:
            try:
                customer = Customer.objects.get(id=request.user.id)
                cart_item = OrderDetail.objects.get(id=id, cart__user=customer)
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
                customer = Customer.objects.get(id=request.user.id)
                cart_item = OrderDetail.objects.get(id=id, cart__user=customer)
                serializer = CartItemSerializer2(cart_item, data=request.data, partial=True)
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
        serializer = CartItemSerializer(data=request.data)
        print(request.data)
        customer = Customer.objects.get(id=request.user.id)
        cart = Cart.objects.filter(user=customer, status=False).first()

        if serializer.is_valid():
            product_id = serializer.validated_data.get('id')
            quantity = serializer.validated_data.get('number')
            my_product = Product.objects.get(id=product_id)
            order = OrderDetail(product=my_product, quantity=quantity)
            if cart:
                order.cart = cart
                order.save()
                return Response({'details': "added"}, status=status.HTTP_201_CREATED)
            else:
                order.cart = Cart.objects.create(user=customer)
                order.save()
                return Response({'details': "added"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def cart_items_view(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=customer, status=False)
        return render(request, 'cart_items.html', {'cart': cart})
    else:

        cart_items = request.session.get('cart_items', [])
        cart_items = [
            {
                'product': Product.objects.get(id=item['product_id']),
                'quantity': item['quantity']
            }
            for item in cart_items
        ]
        context = {'cart_items': cart_items}
        return render(request, 'cart_items.html', context)


@login_required
def finalize_cart(request):
    cart_items = request.session.get('cart_items', [])
    if cart_items:
        customer = Customer.objects.get(id=request.user.id)
        cart = Cart.objects.get_or_create(user=customer, status=False)[0]

        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            OrderDetail.objects.create(cart=cart, product=product, quantity=item['quantity'])
        del request.session['cart_items']
    return redirect('orders:api:cart_items_view')


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def is_authenticated_view(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


def not_authenticated(request):
    return JsonResponse({'is_authenticated': False})


from .serializers import *


class ProductSingleShow(APIView):

    def post(self, request):
        data = request.data
        print(data)
        serializer = ProductDetailSerializer(data=data)
        if serializer.is_valid():
            new = {'product_id': serializer.validated_data.get('id'),
                   'quantity': serializer.validated_data.get('number')}
            product = Product.objects.get(id=serializer.validated_data.get('id'))
            quantity = serializer.validated_data.get('quantity')
            print('product', product.name)
            return Response(data={'added': 'added'})
        print('this is error')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        product_id = request.query_params.get('product_id')
        quantity = request.query_params.get('quantity')
        print('product single show....')

        if product_id and quantity:
            try:
                product = Product.objects.get(id=product_id)
                return Response(data={'product': product.name, 'price': product.price, 'quantity': quantity,
                                      'total': int(product.price) * int(quantity), 'product_id': product.id,
                                      'id': product.id})
            except Product.DoesNotExist:
                return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render


def product_details_view(request):
    return render(request, 'product_details.html')


from django.shortcuts import redirect

from orders.models import OrderDetail, Product
from django.http import HttpResponse

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# @login_required
# def create_order(request):
#     product_id = request.GET.get('productId')
#     quantity = request.GET.get('quantity')
#     print('this is product id ',product_id)
#     print('this is quantity',quantity)
#     print('hiiiiiiiiiiiiiii')
#
#     if product_id and quantity:
#         try:
#             product = Product.objects.get(id=product_id)
#             total_price = product.price * int(quantity)
#
#             customer = Customer.objects.get(id=request.user.id)
#             new_orders = OrderDetail(
#                 product=product,
#                 quantity=quantity,
#                 total_price=total_price
#             )
#
#             cart = Cart.objects.filter(user=customer, status=False).first()
#             if cart:
#                 new_orders.cart = cart
#                 new_orders.save()
#             else:
#                 new_orders.cart = Cart.objects.create(user=customer)
#                 new_orders.save()
#
#             return redirect('website:landing_page')
#         except Product.DoesNotExist:
#             return HttpResponse("Product does not exist", status=404)
#
#     return HttpResponse("Invalid request", status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CartItemSerializer, CartItemSerializer2

# class CreateOrder(APIView):
#     def get(self, request):
#         print('this is create order get method')
#         if request.user.is_authenticated:
#             customer = Customer.objects.get(id=request.user.id)
#             cart_items = OrderDetail.objects.filter(cart__user=customer, processed=False)
#             serializer = CartItemSerializer2(cart_items, many=True)
#             return Response(serializer.data)
#         else:
#             cart_items = request.session.get('cart_items', [])
#             return Response(cart_items)
#
#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data)
#         print('this is show in create orders:', request.data)
#         customer = Customer.objects.get(id=request.user.id)
#         cart = Cart.objects.filter(user=customer, status=False).first()
#
#         if serializer.is_valid():
#             product_id = serializer.validated_data.get('id')
#             quantity = serializer.validated_data.get('number')
#             my_product = Product.objects.get(id=product_id)
#             order = OrderDetail(product=my_product, quantity=quantity)
#             if cart:
#                 order.cart = cart
#                 order.save()
#                 return Response({'details': "added"}, status=status.HTTP_201_CREATED)
#             else:
#                 order.cart = Cart.objects.create(user=customer)
#                 order.save()
#                 return Response({'details': "added"}, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse


def order_create(request, id, quantity):
    print('Product ID:', id)
    print('Quantity:', quantity)
    print('User:', request.user)
    print(type(id))

    product = Product.objects.get(id=id)

    total_price = product.price * int(quantity)

    customer = Customer.objects.get(id=request.user.id)
    new_orders = OrderDetail(
        product=product,
        quantity=quantity,
        total_price=total_price
    )

    cart = Cart.objects.filter(user=customer, status=False).first()
    if cart:
        new_orders.cart = cart
        new_orders.save()
    else:
        new_orders.cart = Cart.objects.create(user=customer)
        new_orders.save()

    return redirect('website:landing_page')

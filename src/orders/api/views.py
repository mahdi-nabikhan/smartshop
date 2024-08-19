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

from .serializers import CartItemSerializer


class CartItemAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(id=request.user.id)
            print(customer)
            cart_items = OrderDetail.objects.filter(cart__user=customer)
            serializer = CartItemSerializer(cart_items, many=True)
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
            customer = Customer.objects.get(id=request.user.id)
            cart = Cart.objects.get_or_create(user=customer)[0]
            product = Product.objects.get(id=request.data['product_id'])
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


def cart_items_view(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request, 'cart_items.html')
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
        cart = Cart.objects.get_or_create(user=customer)[0]
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            OrderDetail.objects.create(cart=cart, product=product, quantity=item['quantity'])
        del request.session['cart_items']
    return redirect('cart_items_view')


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def is_authenticated(request):
    return JsonResponse({'is_authenticated': True})


def not_authenticated(request):
    return JsonResponse({'is_authenticated': False})


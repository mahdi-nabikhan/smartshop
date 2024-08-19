from rest_framework import serializers
from orders import *
from customers.models import Customer
from orders.models import *
from website.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart'] = CartSerializer(instance.cart).data
        response['product'] = ProductSerializer(instance.product).data
        return response

    def get_image_url(self, obj):
        return obj.image.url

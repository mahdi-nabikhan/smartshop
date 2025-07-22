from django.contrib import admin
from .models import Customer, Address, Product, Cart, OrderDetail, Bill
from customers.models import *


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1


class CartInline(admin.TabularInline):
    model = Cart
    extra = 1


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


class BillInline(admin.TabularInline):
    model = Bill
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    inlines = [OrderDetailInline, BillInline]
    search_fields = ('user', 'created_at', 'status')


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'status', 'total_price', 'processed')
    search_fields = ('cart', 'product', 'quantity', 'status', 'total_price', 'processed')


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('cart', 'created_at', 'address', 'status')
    search_fields = ('cart', 'created_at', 'address', 'status')

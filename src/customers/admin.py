from django.contrib import admin
from .models import Customer, Address, Comments
from django.contrib import admin
from .models import Customer, Address, Comments
from orders.models import *


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1


class CartInline(admin.TabularInline):
    model = Cart
    extra = 1


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    inlines = [AddressInline, CommentsInline, CartInline]
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')

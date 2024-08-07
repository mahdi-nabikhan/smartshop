from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__id', 'product__name')


admin.site.register(OrderDetail, OrderDetailAdmin)

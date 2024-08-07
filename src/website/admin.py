from django.contrib import admin
from .models import Category, Product, ProductImages, ProductRate


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')
    search_fields = ('title',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity_in_stock', 'price', 'discount', 'category', 'store')
    search_fields = ('name', 'category__title', 'store__name')


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product_image', 'product', 'title', 'description')
    search_fields = ('product__name', 'title')


class ProductRateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'product')
    search_fields = ('product__name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(ProductRate, ProductRateAdmin)

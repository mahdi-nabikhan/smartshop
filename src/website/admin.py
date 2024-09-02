from django.contrib import admin
from .models import Category, Discount, Product, ProductImages, ProductRate


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductRateInline(admin.TabularInline):
    model = ProductRate
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_parent')
    inlines = [ProductInline, ]
    search_fields = ('title', 'description')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_type', 'value')
    search_fields = ('discount_type', 'value')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity_in_stock', 'price', 'price_after', 'category', 'store')
    inlines = [ProductImagesInline, ProductRateInline]
    search_fields = ('category', 'store', 'name', 'price')


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'product')
    search_fields = ('title', 'product')


@admin.register(ProductRate)
class ProductRateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'product', 'total_rate')
    search_fields = ('product', 'rate')

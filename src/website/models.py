from django.db import models
from vendors.models import Store


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category_image')
    description = models.TextField()
    is_parent=models.ForeignKey('self', blank=True, null=True, related_name='parent', on_delete=models.CASCADE)


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        cash = 'cash', 'Cash'
        percentage = 'percentage', 'Percentage'

    discount_type = models.CharField(max_length=250, choices=DiscountType.choices)
    value = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    quantity_in_stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.OneToOneField(Discount, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')

    def __str__(self):
        return f"{self.name} {self.description}"


class ProductImages(models.Model):
    product_image = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_for_product')
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} {self.product.name}'


class ProductRate(models.Model):
    rate = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_rate')

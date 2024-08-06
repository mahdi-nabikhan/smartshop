from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    quantity_in_stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()

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
    rate=models.PositiveIntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_rate')
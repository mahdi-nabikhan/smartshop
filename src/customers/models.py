from django.db import models
from ..accounts.models import User
from ..website import Product


# Create your models here.


class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return f"{self.user} {self.country} {self.city}"


class Comments(models.Model):
    descriptions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_customer')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_customer')




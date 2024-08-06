from django.db import models
from accounts.models import User
from website.models import Product


# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


class OrderDetail(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='order_cart')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_product')
    quantity = models.PositiveIntegerField()



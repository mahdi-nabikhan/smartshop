from django.db import models
from customers.models import Customer
from website.models import Product


# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_cart')
    status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


class OrderDetail(models.Model):
    class Status(models.TextChoices):
        pending = 'P', 'Pending'
        confirmed = 'C', 'Confirmed'
        rejected = 'R', 'Rejected'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.PositiveIntegerField()
    status = models.CharField(choices=Status.choices, default=Status.pending, max_length=20)

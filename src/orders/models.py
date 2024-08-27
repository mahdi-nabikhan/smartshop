from django.db import models
from customers.models import Customer, Address
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

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.PositiveIntegerField()
    status = models.CharField(choices=Status.choices, default=Status.pending, max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    processed = models.BooleanField(default=False)

    def get_total_price(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        return super(OrderDetail, self).save(*args, **kwargs)


class Bill(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='bill_cart')
    created_at = models.DateField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='bill_address')
    status = models.BooleanField(default=False)

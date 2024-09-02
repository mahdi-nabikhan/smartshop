from django.db import models
from accounts.models import User
from website.models import Product


# Create your models here.


class Customer(User):
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return f" {self.country} {self.city}"


class Comments(models.Model):
    class Status(models.TextChoices):
        pending = 'P', 'Pending'
        confirmed = 'C', 'Confirmed'
        rejected = 'R', 'Rejected'

    descriptions = models.TextField()
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comment_customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_customer')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replay', on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, default=Status.pending, max_length=20)

    def __str__(self):
        return f"{self.user} {self.product} {self.status}"

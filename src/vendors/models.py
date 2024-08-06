from django.db import models
from accounts.models import User
from website.models import Product
# Create your models here.


class Store(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='store_owner')
    admin = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='store_admin')
    products=models.ForeignKey(Product,on_delete=models.DO_NOTHING,related_name='store_product')


class StoreRate(models.Model):
    rate=models.PositiveIntegerField()
    store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_rate')


class StoreAddress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    store=models.OneToOneField(Store,on_delete=models.CASCADE,related_name='store_address')
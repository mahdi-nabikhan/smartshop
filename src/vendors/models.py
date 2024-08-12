from django.db import models
from accounts.models import User


# Create your models here.


class Managers(User):
    is_Managers = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name


class Store(models.Model):
    image = models.ImageField(upload_to='store_image')
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Managers, on_delete=models.CASCADE, related_name='store_owner')


class StoreRate(models.Model):
    rate = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_rate')


class StoreAddress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='store_address')


class Admin(User):
    is_admins = models.BooleanField(default=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='admin')


class Operator(User):
    is_operator = models.BooleanField(default=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='operator')

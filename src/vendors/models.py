from django.db import models
from accounts.models import User


# Create your models here.
class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class Operator(User):
    class Meta:
        proxy = True
        verbose_name = 'operator'
        verbose_name_plural = 'operators'


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_owner')
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, related_name='store_admin', null=True, blank=True)
    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING, related_name='store_operator', null=True,
                                 blank=True)


class StoreRate(models.Model):
    rate = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_rate')


class StoreAddress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='store_address')

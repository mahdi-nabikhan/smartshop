from django.db import models
from django.db.models import Sum

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
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.name


class StoreRate(models.Model):
    rate = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_rate')
    total_rate = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_rate = self.get_total_rate()
        return super().save(*args, **kwargs)

    def get_total_rate(self):
        total = StoreRate.objects.filter(store=self.store).aggregate(total=Sum('rate'))['total']
        return total

    def __str__(self):
        return f'{self.store} {self.rate}'


class StoreAddress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='store_address')

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.store}'


class Admin(User):
    is_admins = models.BooleanField(default=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='my_admin')

    def __str__(self):
        return f'{self.store} {self.first_name}'


class Operator(User):
    is_operator = models.BooleanField(default=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='operator')

    def __str__(self):
        return f'{self.store} {self.first_name}'

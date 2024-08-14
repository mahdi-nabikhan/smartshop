from django.contrib import admin

from .models import *


# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(StoreAddress)
class StoreAddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'country')


@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'country')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('description', 'user')

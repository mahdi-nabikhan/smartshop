from django.contrib import admin
from .models import Managers, Store, StoreRate, StoreAddress, Admin, Operator


class StoreRateInline(admin.TabularInline):
    model = StoreRate
    extra = 1


class StoreAddressInline(admin.TabularInline):
    model = StoreAddress
    extra = 1


class AdminInline(admin.TabularInline):
    model = Admin
    extra = 1


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 1

class StoreInline(admin.TabularInline):
    model = Store
    extra = 1


@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')
    inlines = [AdminInline, OperatorInline,StoreInline]
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description')
    inlines = [StoreRateInline, StoreAddressInline,OperatorInline,AdminInline]
    search_fields = ('name', 'owner', 'description')



@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'store')
    search_fields = ('email', 'first_name', 'last_name', 'store')

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'store')
    search_fields = ('email', 'first_name', 'last_name', 'store')
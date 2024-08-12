from django.shortcuts import render
from django.views import View
from vendors.models import Store, StoreAddress

from django.shortcuts import render
from django.views import View
from vendors.models import Store, StoreAddress, Managers,Admin


class ManagerProfile(View):
    template_name = 'admins/admin_panel.html'

    def get(self, request):
        user = request.user
        is_manager = Managers.objects.filter(id=user.id).exists()

        if is_manager:
            store = Store.objects.get(owner=user)
            address = StoreAddress.objects.filter(store=store)
            return render(request, self.template_name, {'store': store, 'addresses': address, 'is_manager': is_manager})
        return render(request, self.template_name)


class AdminProfile(View):
    template_name = 'admins/admin_panel.html'

    def get(self, request):
        user=request.user
        is_admin=Admin.objects.filter(id=user.id).exists()
        print(is_admin)
        if is_admin:
            store=Store.objects.get(my_admin=user)
            address = StoreAddress.objects.filter(store=store)
            context = {'store': store, 'addresses': address, 'is_admin': is_admin}
            return render(request, self.template_name, context)
        return render(request, self.template_name)

from django.shortcuts import render
from django.views import View
from vendors.models import Store, StoreAddress

from django.shortcuts import render
from django.views import View
from vendors.models import Store, StoreAddress, Managers, Admin, Operator


class ManagerProfile(View):
    template_name = 'admins/admin_panel.html'

    def get(self, request):
        user = request.user
        is_manager = Managers.objects.filter(id=user.id).exists()
        is_admin = Admin.objects.filter(id=user.id).exists()
        is_operator = Operator.objects.filter(id=user.id).exists()
        if is_manager:
            store = Store.objects.get(owner=user)
            address = StoreAddress.objects.filter(store=store)
            return render(request, self.template_name, {'store': store, 'addresses': address, 'is_manager': is_manager})

        elif is_admin:
            store = Store.objects.get(my_admin=user)
            address = StoreAddress.objects.filter(store=store)
            context = {'store': store, 'addresses': address, 'is_admin': is_admin}
            return render(request, self.template_name, context)
        elif is_operator:
            store = Store.objects.get(operator=user)
            address = StoreAddress.objects.filter(store=store)
            context = {'store': store, 'addresses': address, 'is_operator': is_operator}
            return render(request, self.template_name, context)
        return render(request, self.template_name)

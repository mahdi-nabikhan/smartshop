from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


from vendors.models import *


# Create your views here.


class ManagerProfile(View):
    template_name = 'admin_panel.html'

    def get(self, request):
        user = request.user
        if request.user.role == 'admin':
            store = Store.objects.get(admin=user)
            address = StoreAddress.objects.filter(store=store)
            return render(request, self.template_name, {'store': store, 'address': address})
        elif request.user.role == 'manager':
            store = Store.objects.get(owner=user)
            address = StoreAddress.objects.filter(store=store)
            return render(request, self.template_name, {'store': store,'address': address})

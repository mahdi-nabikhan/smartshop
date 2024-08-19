from django import forms
from orders.models import *


class QuantityForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['quantity']

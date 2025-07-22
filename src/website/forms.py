from django import forms
from orders.models import *
from .models import *


class QuantityForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['quantity']


class AddRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRate
        fields = ['rate']

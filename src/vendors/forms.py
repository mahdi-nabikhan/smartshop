from django import forms
from .models import Store,StoreAddress


class RegistrationStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name','description']


class AddressStoreForm(forms.ModelForm):
    class Meta:
        model = StoreAddress
        fields = ['country','city','street']

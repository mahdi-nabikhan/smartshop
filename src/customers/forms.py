from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Password2', max_length=100)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords must match')
        return password2


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street']

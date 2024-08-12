from django import forms
from .models import Store, StoreAddress, Managers, Admin


class RegistrationManagerForms(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Managers
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password = self.cleaned_data.get('password')
        if password2 != password:
            raise forms.ValidationError("Passwords don't match")
        return password2


class RegistrationStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'image']


class AddressStoreForm(forms.ModelForm):


    class Meta:
        model = StoreAddress
        fields = ['country', 'city', 'street']


class AdminRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password = self.cleaned_data.get('password')
        if password2 != password:
            raise forms.ValidationError("Passwords don't match")
        return password2

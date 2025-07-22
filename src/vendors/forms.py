from django import forms
from .models import Store, StoreAddress, Managers, Admin, Operator, StoreRate
from website.models import Product, ProductImages, Discount
from orders.models import OrderDetail


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


class AddProductForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity_in_stock', 'price', 'category']


class AddImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['product_image']


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity_in_stock', 'price', 'category', 'discount']

    def save(self, commit=True):
        product = super().save(commit=False)
        if product.discount:
            if product.discount.discount_type == 'cash':
                product.price_after = product.price - product.discount.value
            if product.discount.discount_type == 'percentage':
                product.price_after = product.price - (product.price * (product.discount.value // 100))
        if commit:
            product.save()
        return product


class UpdateStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description']


class UpdateManagersForm(forms.ModelForm):
    class Meta:
        model = Managers
        fields = ['first_name', 'last_name', 'email', 'phone']


class AddDiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'


class RegisterOperators(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Operator
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password = self.cleaned_data.get('password')
        if password2 != password:
            raise forms.ValidationError("Passwords don't match")
        return password2


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['status']


class StoreRateForm(forms.ModelForm):
    class Meta:
        model = StoreRate
        fields = ('rate',)


class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'email', 'phone']


class UpdateOperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['first_name', 'last_name', 'email', 'phone']

from django import forms
from accounts.models import User


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Password2', max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords must match')
        return password2

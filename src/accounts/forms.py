from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(label='Password', max_length=100)

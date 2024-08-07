from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

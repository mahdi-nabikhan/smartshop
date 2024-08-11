from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(label='Password', max_length=100)


from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=13)



from django import forms

class VerificationCodeForm(forms.Form):

    code = forms.CharField(max_length=6)

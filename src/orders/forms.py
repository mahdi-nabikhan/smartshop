# forms.py
from django import forms
from customers.models import Address


# forms.py


class AddressSelectionForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        empty_label="Select Address",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)

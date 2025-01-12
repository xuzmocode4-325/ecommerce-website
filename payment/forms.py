from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'surname', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude = ['user', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Bonnie'}),
            'surname': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Green'}),
            'address1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Street'}),
            'address2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Suburb'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your State / Province'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Zip / Area Code'}),
        }
        labels = {
            'address1': 'Street Address',
            'address2': 'Suburb',
            'state': 'State / Province'
        }



from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
       
    class Meta:
        model = ShippingAddress
        fields = ['name', 'surname', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude = ['user', 'email']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'address1': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'address2': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'zipcode': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
        }



from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


# Registration Form
class CreateUserForm(UserCreationForm):
     
    email = forms.EmailField(
        label='Email Address',
        help_text='Required. No spam.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
            }
        ),
        required=True,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-input',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input'
            }
        )
    )


class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta: 
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']
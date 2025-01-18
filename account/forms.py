from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from . models import Profile

# Registration Form
class CreateUserForm(UserCreationForm):
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
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}))
    class Meta: 
        model = User
        fields = ['profile_picture','username', 'email']
        exclude = ['password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
        }

    password = None

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
            }
        ),
        required=True,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('An account with this email already exists.')
        
        return email
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, profile_picture=self.cleaned_data['profile_picture'])
            profile.save()
        return user
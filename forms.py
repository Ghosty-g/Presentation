from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+919876543210'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError(
                "Enter a valid phone number (7–15 digits, optional +)."
            )
        return phone




class LoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': visible.label
            })



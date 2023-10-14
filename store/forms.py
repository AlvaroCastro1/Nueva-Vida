from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    telefono = forms.CharField(max_length=10, required=True, help_text='Required. Enter your phone number.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2')

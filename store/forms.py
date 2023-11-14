from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    telefono = forms.CharField(max_length=10, required=True, help_text='Required. Enter your phone number.')

    def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            placeH = ["Nombre de Usuario", "Nombres", "Apellidos", "Email", "Teléfono", "Constraseña", "Confirmar Constraseña"]
            i=0
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'controls'
                visible.field.widget.attrs['placeholder'] = placeH[i]
                i+=1

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2')


from django import forms
from django.contrib.auth.forms import UserChangeForm

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

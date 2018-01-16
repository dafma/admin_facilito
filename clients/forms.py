from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget= forms.PasswordInput())


class CreateUSerForm(forms.ModelForm):
    username = forms.CharField(max_length=20,
                               error_messages= {'required': 'El username es requerido',
                                                'unique': 'El username ya se encuentra registrado',
                                                'invalid':'el usrname es incorrecto'})
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(),
                               error_messages={'required': 'El password es requerido'})
    email = forms.CharField(error_messages={'required': 'El email es requerido', 'invalid': 'ingrese un correo valido'})
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


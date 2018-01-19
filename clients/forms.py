from django import forms
from django.contrib.auth.models import User

"""
constant"""
ERROR_MESSAGE_USER =  {'required': 'El username es requerido',
                                                'unique': 'El username ya se encuentra registrado',
                                                'invalid':'el usrname es incorrecto'}
ERROR_MESSAGE_PASSWORD = {'required': 'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required': 'El email es requerido', 'invalid': 'ingrese un correo valido'}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget= forms.PasswordInput())


class CreateUSerForm(forms.ModelForm):
    username = forms.CharField(max_length=20,error_messages= ERROR_MESSAGE_USER)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(),error_messages=ERROR_MESSAGE_PASSWORD)
    email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20,error_messages=ERROR_MESSAGE_USER)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(),error_messages=ERROR_MESSAGE_PASSWORD)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

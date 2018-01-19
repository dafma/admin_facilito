from django import forms
from django.contrib.auth.models import User

"""
validacion por functions
"""
def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError("El password debe de contener por lo menos 5 caracteres, desde una func")


"""
constant"""
ERROR_MESSAGE_USER =  {'required': 'El username es requerido',
                                                'unique': 'El username ya se encuentra registrado',
                                                'invalid':'el usrname es incorrecto'}
ERROR_MESSAGE_PASSWORD = {'required': 'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required': 'El email es requerido', 'invalid': 'ingrese un correo valido'}

class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget= forms.PasswordInput())


class CreateUSerForm(forms.ModelForm):
    username = forms.CharField(max_length=20,error_messages= ERROR_MESSAGE_USER)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(),error_messages=ERROR_MESSAGE_PASSWORD, validators=[must_be_gt])
    email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20,error_messages=ERROR_MESSAGE_USER)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class EditPasswordForm(forms.Form):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages=ERROR_MESSAGE_PASSWORD)
    new_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages=ERROR_MESSAGE_PASSWORD)
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages=ERROR_MESSAGE_PASSWORD)

    # validacion los passwords no son los mismos
    def clean(self):
        clean_data = super(EditPasswordForm, self).clean()
        password1 = clean_data['new_password']
        password2 = clean_data['repeat_password']

        if password1 != password2:
            raise forms.ValidationError('los passwords no son los mismos')






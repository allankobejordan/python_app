from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm): # Formulário para o registro padrão (página /accounts/register/)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UsuarioForm(forms.ModelForm): # Formulário para o cadastro interno (usado por quem já está logado)
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
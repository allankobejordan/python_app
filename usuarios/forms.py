from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CadastroUsuarioForm(UserCreationForm):
    nome = forms.CharField(
        max_length=30,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome'})
    )
    sobrenome = forms.CharField(
        max_length=30,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu sobrenome'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'})
    )
    cpf = forms.CharField(
        max_length=14,
        label='CPF',
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'})
    )

    class Meta:
        model = User
        fields = ()  # ← aqui deixamos vazio porque estamos lidando com campos manualmente

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf = re.sub(r'\D', '', cpf)  # Remove tudo que não for número

        if not re.match(r'^\d{11}$', cpf):
            raise ValidationError("CPF inválido. Deve conter 11 dígitos numéricos.")

        if User.objects.filter(username=cpf).exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get("password1")
        senha2 = cleaned_data.get("password2")

        if senha1 and senha2 and senha1 != senha2:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = User()
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['sobrenome']
        user.username = re.sub(r'\D', '', self.cleaned_data['cpf'])
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])  # seta a senha corretamente

        if commit:
            user.save()
        return user

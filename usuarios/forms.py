from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cpf = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    
    PERFIL_CHOICES = [('comum', 'Comum'), ('master', 'Master')]
    perfil = forms.ChoiceField(choices=PERFIL_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'cpf', 'telefone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        user_logado = kwargs.pop('user_logado', None)
        super().__init__(*args, **kwargs)
        
        if not user_logado or not user_logado.perfilusuario.perfil == 'master':
            self.fields.pop('perfil')
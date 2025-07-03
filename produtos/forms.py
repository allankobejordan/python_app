from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'tamanho', 'imagem', 'quantidade']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'required': False}),
        }
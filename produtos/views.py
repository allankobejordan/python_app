from django.shortcuts import render,  redirect
from django.contrib import messages 
from .forms import ProdutoForm
from .models import Produto

def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco', '0').replace(',', '.')
        tamanho = request.POST.get('tamanho')
        imagem = request.FILES.get('imagem')

        if nome and preco:
            try:
                Produto.objects.create(
                    nome=nome,
                    descricao=descricao,
                    preco=preco,
                    tamanho=tamanho,
                    imagem=imagem
                )
                messages.success(request, "✅ Produto cadastrado com sucesso! 👕✨")
            except Exception as e:
                messages.error(request, f"❌ Erro ao cadastrar produto 😵: {str(e)}")
        else:
            messages.warning(request, "⚠️ Preencha todos os campos obrigatórios! 📝")

    return render(request, 'produtos/produtos.html')  # aqui é só o form

def listar_produtos(request):
    produtos = Produto.objects.all().order_by('-id')
    return render(request, 'home.html', {'produtos': produtos})
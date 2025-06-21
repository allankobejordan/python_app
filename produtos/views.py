from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProdutoForm
from .models import Produto
from django.core.paginator import Paginator

# ✅ Agora chamado catalogo (era: inicio)
def catalogo(request):
    produtos = Produto.objects.all()

    query = request.GET.get('q')
    tamanho = request.GET.get('tamanho')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    ordenar = request.GET.get('ordenar')

    if query:
        produtos = produtos.filter(nome__icontains=query)

    if tamanho:
        produtos = produtos.filter(tamanho=tamanho)

    if preco_min:
        try:
            produtos = produtos.filter(preco__gte=float(preco_min))
        except ValueError:
            pass

    if preco_max:
        try:
            produtos = produtos.filter(preco__lte=float(preco_max))
        except ValueError:
            pass

    if ordenar == 'preco_asc':
        produtos = produtos.order_by('preco')
    elif ordenar == 'preco_desc':
        produtos = produtos.order_by('-preco')
    elif ordenar == 'nome_asc':
        produtos = produtos.order_by('nome')
    elif ordenar == 'nome_desc':
        produtos = produtos.order_by('-nome')

    paginator = Paginator(produtos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'produtos/catalogo.html', {
        'page_obj': page_obj
    })

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

    return render(request, 'produtos/produtos.html')

# ✅ Listagem administrativa com ações
def listar_produtos(request):
    produtos = Produto.objects.all().order_by('-id')
    return render(request, 'produtos/listar_produtos.html', {'produtos': produtos})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtos:listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form})

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
    return redirect('produtos:listar_produtos')

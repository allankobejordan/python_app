from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProdutoForm
from .models import Produto
from django.core.paginator import Paginator

# ✅ Exibe o catálogo com filtros
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

    return render(request, 'produtos/catalogo.html', {
        'page_obj': page_obj
    })

# ✅ Cadastro de produto
def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco', '0').replace(',', '.')
        tamanho = request.POST.get('tamanho')
        imagem = request.FILES.get('imagem')
        quantidade = int(request.POST.get('quantidade'))

        if nome and preco:
            try:
                Produto.objects.create(
                    nome=nome,
                    descricao=descricao,
                    preco=preco,
                    tamanho=tamanho,
                    quantidade=quantidade,
                    imagem=imagem
                )
                messages.success(request, "✅ Produto cadastrado com sucesso! 👕✨")
            except Exception as e:
                messages.error(request, f"❌ Erro ao cadastrar produto 😵: {str(e)}")
        else:
            messages.warning(request, "⚠️ Preencha todos os campos obrigatórios! 📝")

    return render(request, 'produtos/produtos.html')

# ✅ Listagem de produtos para admin
def listar_produtos(request):
    produtos = Produto.objects.all().order_by('-id')
    return render(request, 'produtos/listar_produtos.html', {'produtos': produtos})

# ✅ Editar produto
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

# ✅ Excluir produto
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
    return redirect('produtos:listar_produtos')

# ✅ Adicionar ao carrinho com checagem de estoque
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    quantidade_requisitada = int(request.POST.get('quantidade', 1))

    if produto.quantidade == 0:
        messages.error(request, "Produto indisponível no momento.")
        return redirect('produtos:catalogo')
    
    if quantidade_requisitada > produto.quantidade:
        messages.error(request, "Quantidade solicitada maior que o estoque disponível.")
        return redirect('produtos:catalogo')
    
    carrinho = request.session.get("carrinho", {})

    if str(produto_id) in carrinho:
        nova_quantidade = carrinho[str(produto_id)]['quantidade'] + quantidade_requisitada
        if nova_quantidade > produto.quantidade:
            messages.warning(request, "Você não pode adicionar mais do que temos em estoque.")
            return redirect('produtos:catalogo')
        carrinho[str(produto_id)]['quantidade'] = nova_quantidade
    else:
        carrinho[str(produto_id)] = {
            'nome': produto.nome,
            'preco': float(produto.preco),
            'quantidade': quantidade_requisitada,
            'tamanho': produto.tamanho,
            'imagem_url': produto.imagem.url if produto.imagem else ''
        }

    request.session['carrinho'] = carrinho
    messages.success(request, f"{produto.nome} adicionado ao carrinho!")
    return redirect('produtos:catalogo')

# ✅ Visualizar carrinho
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = 0
    itens_processados = {}

    for id, item in carrinho.items():
        preco_unit = float(item['preco'])
        subtotal = preco_unit * item['quantidade']
        total += subtotal
        itens_processados[id] = {
            **item,
            'subtotal': round(subtotal, 2)
        }

    return render(request, 'produtos/carrinho.html', {
        'carrinho': itens_processados,
        'total': round(total, 2)
    })

# ✅ Remover item do carrinho
def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})

    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]
        request.session['carrinho'] = carrinho
        messages.success(request, "Item removido do carrinho.")
    return redirect('produtos:ver_carrinho')

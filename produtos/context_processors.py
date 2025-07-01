# produtos/context_processors.py

def total_itens_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total_itens = sum(item['quantidade'] for item in carrinho.values())
    return {
        'total_itens_carrinho': total_itens
    }

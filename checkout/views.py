from django.shortcuts import render, redirect
from django.contrib import messages

def checkout(request):
    carrinho = request.session.get('carrinho',{})
    if not carrinho:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('home')
    
    total = sum(item['quantidade'] * item['preco'] for item in carrinho.values())

    return render(request, 'checkout.html', {
        'carrinho': carrinho,
        'total': total,
    })

# Create your views here.

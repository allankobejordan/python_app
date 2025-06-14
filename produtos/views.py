from django.shortcuts import render

def cadastrar_produto(request):
    return render(request, 'produtos/produtos.html')

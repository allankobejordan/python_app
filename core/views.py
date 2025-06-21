from django.core.paginator import Paginator
from django.shortcuts import render
from produtos.models import Produto

def home(request):
    produtos_list = Produto.objects.all().order_by('-id')  # Mais recentes primeiro
    paginator = Paginator(produtos_list, 9)  # 9 por página (3x3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})

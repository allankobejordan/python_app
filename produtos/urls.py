from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.catalogo, name='catalogo'),  # 👈 atualizado aqui
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/listar/', views.listar_produtos, name='listar_produtos'),
    path('admin/produtos/excluir/<int:produto_id>/', views.excluir_produto, name="excluir_produto"),
    path('admin/produtos/editar/<int:produto_id>/', views.editar_produto, name="editar_produto"),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),


]

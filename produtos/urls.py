app_name = 'produtos'

from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('', views.listar_produtos, name='listar_produtos'),  # home com o catálogo
]

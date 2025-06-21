from django.urls import path
from .views import (
    cadastrar_usuario,
    confirmar_codigo,
    listar_usuarios,
    editar_usuario,
    excluir_usuario
)

urlpatterns = [
    path('cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('confirmar-codigo/', confirmar_codigo, name='confirmar_codigo'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:id>/', excluir_usuario, name='excluir_usuario'),
]

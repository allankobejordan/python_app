from django.urls import path
from .views import register, listar_usuarios
from .views import register, listar_usuarios, cadastrar_usuario, editar_usuario, excluir_usuario
from . import views


urlpatterns = [
    path('register/', register, name='register'),
    path('listar/', listar_usuarios, name='listar_usuarios'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('confirmar-codigo/', views.confirmar_codigo, name='confirmar_codigo'),
    path('editar/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:id>/', excluir_usuario, name='excluir_usuario')

]

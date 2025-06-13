from django.urls import path
from .views import register, listar_usuarios
from .views import register, listar_usuarios, cadastrar_usuario, editar_usuario


urlpatterns = [
    path('register/', register, name='register'),
    path('listar/', listar_usuarios, name='listar_usuarios'),
    path('cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('editar/<int:user_id>/', editar_usuario, name='editar_usuario'),

]

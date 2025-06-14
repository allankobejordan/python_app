from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
]

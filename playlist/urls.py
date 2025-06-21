from django.urls import path
from . import views

app_name = 'playlist'

urlpatterns = [
    path('gerenciar/', views.gerenciar_musicas, name='gerenciar'),
]

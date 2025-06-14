from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # ⬅️ isso é ESSENCIAL
    path('accounts/', include('usuarios.urls')),  # <-- aqui tá tentando importar
    path('', home, name='home'), # ← home protegida por login
    path('produtos/', include('produtos.urls', namespace='produtos')),
]
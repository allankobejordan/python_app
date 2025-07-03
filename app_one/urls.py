from django.contrib import admin
from django.urls import path, include
from core.views import home
from usuarios.views import send_test_email
from django.conf import settings
from django.conf.urls.static import static  # <- você tinha esquecido de importar isso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('usuarios.urls')),
    path('playlist/', include('playlist.urls')),
    path('', home, name='home'),
    path('produtos/', include('produtos.urls')),
    path('teste-email/', send_test_email, name='teste_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

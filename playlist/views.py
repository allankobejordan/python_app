from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Musica
from .forms import MusicaForm

@login_required
def gerenciar_musicas(request):
    if not request.user.perfilusuario.perfil == 'master':
        return HttpResponseForbidden("Acesso negado")

    musicas = Musica.objects.all()
    
    if request.method == 'POST':
        form = MusicaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('playlist:gerenciar')
    else:
        form = MusicaForm()

    return render(request, 'playlist/gerenciar.html', {'form': form, 'musicas': musicas})

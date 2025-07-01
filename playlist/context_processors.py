from .models import Musica

def playlist_musicas(request):
    return {
        'musicas_playlist': Musica.objects.all()
    }

from django.db import models

class Musica(models.Model):
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='musicas/')  # Vai para MEDIA_ROOT/musicas/
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['ordem']

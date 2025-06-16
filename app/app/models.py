import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Ponto(models.Model):
    TIPO_CHOICES = [
        ('AEROPORTO', 'AEROPORTO'),
        ('BUSDOOR', 'BUSDOOR'),
        ('CONTAINERS', 'CONTAINERS'),
        ('EMPENAS', 'EMPENAS'),
        ('FRONT-LIGHT', 'FRONT-LIGHT'),
        ('MEGA-PAINEL', 'MEGA-PAINEL'),
        ('MOBILIÁRIO URBANO', 'MOBILIÁRIO URBANO'),
        ('OUTDOOR', 'OUTDOOR'),
        ('PAINÉIS RODOVIÁRIO', 'PAINÉIS RODOVIÁRIO'),
        ('PAINEL DE LED', 'PAINEL DE LED'),
        ('PLACA DE ESQUINA', 'PLACA DE ESQUINA'),
        ('TOP-SIGHT', 'TOP-SIGHT'),
        ('TOTEM / TOTEM DIGITAL', 'TOTEM / TOTEM DIGITAL'),
    ]

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES
    )
    
    ponto = models.CharField(max_length=20)
    local = models.CharField(max_length=100, null=True, blank=True)  # Agora opcional
    endereco = models.CharField(max_length=255, null=True, blank=True)
    dimensao = models.CharField(max_length=20, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.ponto} - {self.local}'
    

class ImagemUpload(models.Model):
    imagem = models.ImageField(upload_to='imagens_upload/')  # pasta dentro de /media/
    data_upload = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Remove o arquivo do sistema de arquivos
        if self.imagem and os.path.isfile(self.imagem.path):
            os.remove(self.imagem.path)
        # Apaga o registro do banco
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.imagem.name


@receiver(post_delete, sender=ImagemUpload)
def apagar_arquivo_media(sender, instance, **kwargs):
    if instance.imagem and os.path.isfile(instance.imagem.path):
        os.remove(instance.imagem.path)


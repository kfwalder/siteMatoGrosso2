from django.db import models

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
    local = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    dimensao = models.CharField(max_length=20)
    link = models.URLField()
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.ponto} - {self.local}'
    
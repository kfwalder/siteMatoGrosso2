from django.contrib import admin
from .models import Ponto  # Import the Ponto model

# Register your models here.

@admin.register(Ponto)
class Ponto(admin.ModelAdmin):
    list_display = ('id', 'ponto', 'local', 'tipo', 'dimensao')  # O que vai aparecer na listagem
    search_fields = ('ponto', 'local', 'endereco')              # Para facilitar buscas


from django.contrib import admin
from .models import Ponto, Local, ImagemUpload  # Import the Ponto model

# Register your models here.

@admin.register(Ponto)
class Ponto(admin.ModelAdmin):
    list_display = ('id', 'ponto', 'local', 'tipo', 'dimensao')  # O que vai aparecer na listagem
    search_fields = ('ponto', 'local', 'endereco')              # Para facilitar buscas

@admin.register(ImagemUpload)
class ImagemUpload(admin.ModelAdmin):
    list_display = ('id', 'data_upload', 'imagem')
    search_fields = ('data_upload',)

@admin.register(Local)
class Local(admin.ModelAdmin):
    list_display = ['local']  # O que vai aparecer na listagem
    search_fields = ['local']              # Para facilitar buscas

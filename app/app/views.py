import csv
from django.shortcuts import redirect, render, HttpResponse
from django.template import loader
from .forms import UploadCSVForm
from .models import Ponto
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError


# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {
        'cssExtraHeader': 'py-16',
    }
    return HttpResponse(template.render(context, request))


def locais(request):
    return render(request, 'locais.html')
def contato(request):
    return render(request, 'contato.html')
def blog(request):
    return render(request, 'blog.html')
def sobre(request):
    return render(request, 'sobre.html')


# Cabeçalhos esperados no arquivo
CABEÇALHO_ESPERADO = [
    'Ponto',
    'Tipo',
    'Local',
    'Endereço',
    'Dimensão',
    'Link',
    'Latitude',
    'Longitude',
]


def upload_csv(request):
    mensagem_erro = None
    form = UploadCSVForm()  # Criamos o form logo no início
    linhas_com_erro = []

    if request.method == 'POST':
        if 'importar' in request.POST:
            form = UploadCSVForm(request.POST, request.FILES)
            if form.is_valid():
                arquivo = form.cleaned_data['arquivo']
               #decoded_file = arquivo.read().decode('utf-8').splitlines()
                decoded_file = arquivo.read().decode('utf-8-sig').splitlines()
                reader = csv.reader(decoded_file, delimiter=';')

                cabecalho = next(reader, None)
                if cabecalho is None:
                    mensagem_erro = 'Arquivo CSV vazio.'
                elif [col.strip().lower() for col in cabecalho] != [col.lower() for col in CABEÇALHO_ESPERADO]:
                    mensagem_erro = (
                        f'Cabeçalho inválido.<br>'
                        f'Esperado: {", ".join(CABEÇALHO_ESPERADO)}<br>'
                        f'Recebido: {", ".join(cabecalho)}'
                    )
                else:
                    dict_reader = csv.DictReader(decoded_file, fieldnames=CABEÇALHO_ESPERADO, delimiter=';')
                    next(dict_reader) # Pular a primeira linha manualmente
                    for row in dict_reader:
                        row_normalizado = {k.lower(): v for k, v in row.items()}
                        #print(row_normalizado)  # Debug: Imprime a linha normalizada
                        try:
                            Ponto.objects.update_or_create(
                                ponto=row_normalizado['ponto'],
                                defaults={
                                    'tipo': row_normalizado['tipo'].upper().strip(),
                                    'local': row_normalizado['local'],
                                    'endereco': row_normalizado['endereço'],
                                    'dimensao': row_normalizado['dimensão'],
                                    'link': row_normalizado['link'],
                                    'latitude': row_normalizado['latitude'],
                                    'longitude': row_normalizado['longitude'],
                                }
                            )
                        except (IntegrityError, ValidationError) as e:
                            # Salva o erro e a linha
                            linhas_com_erro.append({
                                'linha': row_normalizado,
                                'erro': str(e)
                            })
                    if linhas_com_erro:
                        mensagem_erro = 'Algumas linhas não foram importadas:<br>'
                        for item in linhas_com_erro:
                            linha_str = ', '.join([f'{k}: {v}' for k, v in item['linha'].items()])
                            mensagem_erro += f'<strong>Linha:</strong> {linha_str}<br><strong>Erro:</strong> {item["erro"]}<br><br>'
                        return render(request, 'upload_csv.html', {
                            'form': form,
                            'mensagem_erro': mensagem_erro
                        })
                    return redirect('upload_sucesso')

        elif 'apagar' in request.POST:
            Ponto.objects.all().delete()
            messages.success(request, 'Todos os pontos foram apagados com sucesso.')
            return redirect('upload_csv')
        
    return render(request, 'upload_csv.html', {
        'form': form,
        'mensagem_erro': mensagem_erro
    })

def upload_sucesso(request):
    return render(request, 'upload_sucesso.html')

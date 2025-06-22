import csv
from django.shortcuts import redirect, render, HttpResponse
from django.template import loader
from .forms import UploadCSVForm, ImagemUploadForm 
from .models import Ponto, Local, ImagemUpload
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {
        'cssExtraHeader': 'py-4',
    }
    return HttpResponse(template.render(context, request))


def pontos(request):
    #pontos = Ponto.objects.all().order_by('id')
    #pontos = Ponto.objects.select_related('local_fk').order_by('local_fk__prioridade', 'id')

    local_id = request.GET.get('local')  # pegando o filtro da URL
    pontos = Ponto.objects.select_related('local_fk')
    total_pontos = Ponto.objects.count()
    
    if local_id:
        pontos = pontos.filter(local_fk_id=local_id)

    #pontos = pontos.order_by('local_fk__prioridade', 'id')

    paginator = Paginator(pontos, 12)  # 12 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #locais_disponiveis = Local.objects.order_by('prioridade')
    locais_disponiveis = Local.objects.annotate(
        total_pontos=Count('ponto')
    ).order_by('-total_pontos', 'local')  # ordena do maior para menor

    return render(request, 'pontos.html', {
        'page_obj': page_obj,
        'locais_disponiveis': locais_disponiveis,
        'local_selecionado': int(local_id) if local_id else None,
        'total_pontos': total_pontos,
    })
    

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
                    pontos_vistos = set()

                    for row in dict_reader:
                        row_normalizado = {k.lower(): v.strip() for k, v in row.items()}
                        #print(row_normalizado)  # Debug: Imprime a linha normalizada

                        # Verifica se já vimos esse ponto no mesmo arquivo
                        ponto_nome = row_normalizado['ponto'].strip()
                        if ponto_nome in pontos_vistos:
                            linhas_com_erro.append({
                                'linha': row_normalizado,
                                'erro': f"Ponto duplicado no arquivo: '{ponto_nome}'"
                            })
                            continue
                        pontos_vistos.add(ponto_nome)

                        try:

                            nome_local = row_normalizado['local']
                            local_obj, _ = Local.objects.get_or_create(local=nome_local)

                            Ponto.objects.update_or_create(
                                ponto=row_normalizado['ponto'].strip(),
                                defaults={
                                    'tipo': row_normalizado['tipo'].upper().strip(),
                                    'local_fk': local_obj,
                                    'endereco': row_normalizado['endereço'].strip(),
                                    'dimensao': row_normalizado['dimensão'].strip(),
                                    'link': row_normalizado['link'].strip(),
                                    'latitude': row_normalizado['latitude'].strip(),
                                    'longitude': row_normalizado['longitude'].strip(),
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



def upload_imagem(request):
    if request.method == 'POST':
        form = ImagemUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_uploads')  # ou uma página de sucesso
    else:
        form = ImagemUploadForm()
    return render(request, 'upload.html', {'form': form})

def lista_uploads(request):
    imagens = ImagemUpload.objects.all()
    return render(request, 'lista_uploads.html', {'imagens': imagens})

def secrets(request):
    return render(request, 'secrets.html')

def testeMap(request):
    # Primeiro filtro no banco
    pontos_qs = Ponto.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).exclude(
        latitude='',
        longitude=''
    )

    # Agora validação dos valores no Python
    pontos = []
    for p in pontos_qs:
        try:
            lat = float(p.latitude)
            lng = float(p.longitude)
            if (-90 <= lat <= 90 and -180 <= lng <= 180 and lat != 0 and lng != 0):
                pontos.append(p)
        except (ValueError, TypeError):
            # Ignora se não for número válido
            continue

    return render(request, 'testeMap.html', {
        'pontos': pontos,
    })


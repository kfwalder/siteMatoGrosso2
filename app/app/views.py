from django.shortcuts import render, HttpResponse
from django.template import loader

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

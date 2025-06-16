from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('pontos', views.pontos, name='pontos'),
    path('contato', views.contato, name='contato'),
    path('blog', views.blog, name='blog'),
    path('sobre', views.sobre, name='sobre'),
    path('upload-csv', views.upload_csv, name='upload_csv'),
    path('upload-sucesso', views.upload_sucesso, name='upload_sucesso'),
    path('upload_imagem', views.upload_imagem, name='upload_imagem'),
    path('lista_uploads', views.lista_uploads, name='lista_uploads'),
    path('secrets', views.secrets, name='secrets')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

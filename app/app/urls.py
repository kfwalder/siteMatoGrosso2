from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pontos', views.pontos, name='pontos'),
    path('contato', views.contato, name='contato'),
    path('blog', views.blog, name='blog'),
    path('sobre', views.sobre, name='sobre'),
    path('upload-csv', views.upload_csv, name='upload_csv'),
    path('upload-sucesso', views.upload_sucesso, name='upload_sucesso')
]


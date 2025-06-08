from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('locais', views.locais, name='locais'),
    path('contato', views.contato, name='contato'),
    path('blog', views.blog, name='blog'),
    path('sobre', views.sobre, name='sobre')
]


# arquivo criado manualmente
from django.urls import path
from .views import index, busca, cadastro_escoteiro, cadastro_atividade, cadastro_nrs_registro


urlpatterns = [
    path('', index, name='index_name'),
    path('cadastro_nrs_registro', cadastro_nrs_registro, name='cadastro_nrs_registro'),
    path('busca', busca, name='busca'),
    path('cadastro_escoteiro', cadastro_escoteiro, name='cadastro_escoteiro'),
    path('cadastro_atividade', cadastro_atividade, name='cadastro_atividade'),
]


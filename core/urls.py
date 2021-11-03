# arquivo criado manualmente
from django.urls import path
from .views import index, busca, cad_esc, cadastro_atividade, cadastro_nrs_registro, cad_esc_p2, delete_skill


urlpatterns = [
    path('', index, name='index_name'),
    path('cadastro_nrs_registro', cadastro_nrs_registro, name='cadastro_nrs_registro'),
    path('busca', busca, name='busca'),
    path('cad_esc', cad_esc, name='cad_esc'),
    path('cad_esc_p2/<int:pk>', cad_esc_p2, name='cad_esc_p2'),
    path('cadastro_atividade/<int:pk>', cadastro_atividade, name='cadastro_atividade'),
    path('cadastro_atividade/apagar/<int:pk>', delete_skill, name='delete_skill'),
]


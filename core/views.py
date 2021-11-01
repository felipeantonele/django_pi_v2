from django.shortcuts import render
from django.contrib import messages
from .models import Skills, NumbersRegisters, AssociateData
# from .forms import CadSkillsModelForm, CadScoutModelForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
# Create your views here.
import os, sys


def index(request):
    context = {
        'logado': (str(request.user) != 'AnonymousUser'),
               }
    print('Usuario: '+str(request.user))
    return render(request, 'index.html', context)


def busca(request):
    return render(request, 'busca.html')


def cadastro_nrs_registro(request):
    context = {
        'logado': (str(request.user) != 'AnonymousUser'),
        'upload': False,
        'qtd_cad': 0,
        'qtd_n_cad': 0,
        'deletados': 0,
               }
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            dbframe = pd.read_excel("." + fs.url(filename), sheet_name='nrs_registro')
            context['upload'] = True
            for irow in dbframe.itertuples():
                if str(irow.delete).upper() == 'X':
                    NumbersRegisters.objects.filter(number_register=str(irow.number_register.split('-')[0].strip())).delete()
                    context['deletados'] += 1
                    continue
                if len(NumbersRegisters.objects.filter(number_register=str(irow.number_register.split('-')[0].strip()))) == 0:
                    context['qtd_cad'] += 1
                    obj = NumbersRegisters.objects.create(number_register=irow.number_register.split('-')[0].strip(),
                    function_first=str(irow.function_first).replace('nan', ''), function_second=str(irow.function_second).replace('nan', ''),
                    function_third=str(irow.function_third).replace('nan', ''), section=str(irow.section).replace('nan', ''))
                    obj.save()
                else:
                    context['qtd_n_cad'] += 1
            del dbframe
            os.remove(fs.url(filename).replace('/', ''))
            return render(request, 'cadastro_nrs_registro.html', context)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Erro 1/2: no arquivo: ' + str(fname) + ' - Linha n°' + str(exc_tb.tb_lineno))
        print('Erro 2/2: ' + str(e))
        pass
    #"""
    return render(request, 'cadastro_nrs_registro.html', context)


def cadastro_skill(request):
    """
    Botão de busca para pesquisar uma habilidade, após pesquisa carregue o formulário
    """
    context = {
        #'form': form,
        'lista_skills': Skills.objects.all(),
        'logado': (str(request.user) != 'AnonymousUser'),
    }
    return render(request, 'cadastro_skill.html', context)


def cadastro_escoteiro(request):
    context = {
        #'form': form,
        'lista_scount': NumbersRegisters.objects.all(),
        'logado': (str(request.user) != 'AnonymousUser'),
    }
    return render(request, 'cadastro_escoteiro.html', context)



def cadastro_atividade(request):
    return render(request, 'cadastro_atividade.html')
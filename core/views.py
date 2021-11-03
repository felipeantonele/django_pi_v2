from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Skills, NumbersRegisters, AssociateData
from .forms import NrRegisterForm, AssociateDataModelForm, SkillsModelForm, SearchForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
# Create your views here.
import os, sys, urllib.parse


def index(request):
    context = {
        'logado': (str(request.user) != 'AnonymousUser'),
               }
    #print('Usuario: '+str(request.user))
    return render(request, 'index.html', context)


def busca(request):
    qtd = '10'
    was_searched = False
    text_searched = ''
    form = SearchForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid() and str(form.cleaned_data['text_search']) != '':
            text_searched = str(form.cleaned_data['text_search'])
            #print(text_searched)
            was_searched = True
            results = Skills.objects.filter(name_skill__contains=form.cleaned_data['text_search']).order_by('-id')
        else:
            results = Skills.objects.all().order_by('-id')[:10]
            qtd = len(results)
    else:
        results = Skills.objects.all().order_by('-id')[:10]
        qtd = len(results)
    form1 = SearchForm()
    context = {
        'results': results,
        'logado': (str(request.user) != 'AnonymousUser'),
        'form': form1,
        'was_searched': was_searched,
        'text_searched': text_searched,
        'qtd': qtd,
    }
    return render(request, 'busca.html', context)


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
            dbframe = pd.read_excel(urllib.parse.unquote("." + fs.url(filename)), sheet_name='nrs_registro')
            context['upload'] = True
            for irow in dbframe.itertuples():
                if str(irow.delete).upper() == 'X':
                    nr=str(irow.number_register.split('-')[0].strip())
                    context['deletados'] += 1
                    try:
                        NumbersRegisters.objects.filter(number_register=nr).delete()
                    except:
                        pass
                    try:
                        AssociateData.objects.filter(number_register=str(nr)).delete()
                    except:
                        pass
                    try:
                        Skills.objects.filter(number_register=str(nr)).delete()
                    except:
                        # print('Nenhuma skill')
                        pass

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
            os.remove(urllib.parse.unquote(fs.url(filename)).replace('/', ''))
            return render(request, 'cadastro_nrs_registro.html', context)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Erro 1/2: no arquivo: ' + str(fname) + ' - Linha n°' + str(exc_tb.tb_lineno))
        print('Erro 2/2: ' + str(e))
        pass
    #"""
    return render(request, 'cadastro_nrs_registro.html', context)


def cad_esc(request):
    form = NrRegisterForm(request.POST or None)
    warning = False
    if str(request.method) == 'POST':
        if form.is_valid():
            nr_post = form.cleaned_data['nr']
            #print(nr_post)
            if len(NumbersRegisters.objects.filter(number_register=str(nr_post.split('-')[0].strip()))) != 0:
                id_nr_registro = NumbersRegisters.objects.filter(number_register=str(nr_post.split('-')[0].strip())).values_list('id', flat=True)[0]
                return HttpResponseRedirect('/cad_esc_p2/' + str(id_nr_registro))
                #return redirect(request, id_nr_registro)
            else:
                warning = True
    form = NrRegisterForm()
    context = {
        'form': form,
        'logado': (str(request.user) != 'AnonymousUser'),
        'warning': warning,
    }
    return render(request, 'cadastro_escoteiro.html', context)


def cad_esc_p2(request, pk):
    nr = NumbersRegisters.objects.filter(id=str(pk)).values_list('number_register', flat=True)[0]
    if len(AssociateData.objects.filter(number_register=str(nr))) == 0:
        possui_cad_associatedata = False
    else:
        possui_cad_associatedata = True
    if str(request.method) == 'POST':
        form = AssociateDataModelForm(request.POST)
        if 'delete_associate_data' in request.POST:
            try:
                AssociateData.objects.filter(number_register=str(nr)).delete()
            except:
                #print('Nenhuma associatedata')
                pass
            try:
                Skills.objects.filter(number_register=str(nr)).delete()
            except:
                #print('Nenhuma skill')
                pass
            return HttpResponseRedirect('/')
        elif 'apenas_continuar' in request.POST:
            if len(AssociateData.objects.filter(number_register=str(nr))) == 0:
                messages.error(request, 'Não é possível continuar sem o cadastro')
                form = AssociateDataModelForm(request.POST)
            else:
                associete_cad_id = AssociateData.objects.filter(number_register=str(nr)).values_list('id', flat=True)[0]
                return HttpResponseRedirect('/cadastro_atividade/' + str(associete_cad_id))
        else:
            if form.is_valid():
                if possui_cad_associatedata:
                    AssociateData.objects.filter(number_register=str(nr)).delete()
                form.save()
                associete_cad = form.save(commit=False)
                associete_cad.number_register = str(nr)
                associete_cad.save()
                messages.success(request, 'Dados do escoteiro  ' + str(associete_cad.name) + ' salvo com sucesso')
                form = AssociateDataModelForm(initial={'number_register': str(nr)})
                return HttpResponseRedirect('/cadastro_atividade/' + str(associete_cad.id))
            else:
                messages.error(request, 'Erro ao cadastrar dados do escoteiro')
                form = AssociateDataModelForm(request.POST)
    else:
        if len(AssociateData.objects.filter(number_register=str(nr))) == 0:
            form = AssociateDataModelForm(initial={'number_register': str(nr)})
        else:
            possui_cad_associatedata = True
            fields = ['number_register', 'name', 'responsible_1', 'responsible_2', 'phone', 'email', 'accept_1',
                      'accept_2', 'accept_3']
            d = {}
            for table in fields:
                d[table] = AssociateData.objects.filter(number_register=str(nr)).values_list(table, flat=True)[0]
            form = AssociateDataModelForm(initial=d)
    data1 = NumbersRegisters.objects.get(id=pk)
    context = {
        'form': form,
        'data1': data1,
        'pca': possui_cad_associatedata,
        'logado': (str(request.user) != 'AnonymousUser'),
    }
    return render(request, 'cad_esc_p2.html', context)


def cadastro_atividade(request, pk):
    nr = str(AssociateData.objects.filter(id=str(pk)).values_list('number_register', flat=True)[0])
    if str(request.method) == 'POST':
        if 'delete_skill' in request.POST:
            Skills.objects.filter(id=str(request.POST['delete_skill'])).delete()
            form = SkillsModelForm(initial={'number_register': str(nr)})
        else:
            form = SkillsModelForm(request.POST)
            if form.is_valid():
                form.save()
                skill_cad = form.save(commit=False)
                skill_cad.number_register = str(nr)
                skill_cad.save()
                messages.success(request, 'Competência associada com sucesso - ' + str(skill_cad.name_skill))
                form = SkillsModelForm(initial={'number_register': str(nr)})
            else:
                messages.error(request, 'Erro ao cadastrar Skill')
                form = SkillsModelForm(request.POST)
    else:
        form = SkillsModelForm(initial={'number_register': str(nr)})
    data1 = NumbersRegisters.objects.get(number_register=nr)
    data2 = AssociateData.objects.get(number_register=nr)
    data3 = Skills.objects.filter(number_register=nr)
    #print(data3)
    context = {
        'form': form,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'logado': (str(request.user) != 'AnonymousUser'),
    }

    return render(request, 'cadastro_atividade.html', context)


def delete_skill(request, pk):
    print(request.POST)

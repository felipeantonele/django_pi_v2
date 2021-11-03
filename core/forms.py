from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field
from .models import NumbersRegisters, AssociateData, Skills


types_of_skills = [
    ('Habilidade', 'Habilidade'),
    ('Hobby', 'Hobby'),
    ('Experiência', 'Experiência'),
    ('Profissão', 'Profissão'),
    ]


class NrRegisterForm(forms.Form):
    nr = forms.CharField(label='Número de Registro', max_length=20)


class AssociateDataModelForm(forms.ModelForm):
    class Meta:
        model = AssociateData
        fields = ['name','responsible_1','responsible_2','phone','email','accept_1','accept_2','accept_3']
    #number_register = forms.CharField(label='Número de Registro', max_length=20)
    name = forms.CharField(label='Nome do Escoteiro', max_length=100)
    responsible_1 = forms.CharField(label='Nome do Responsável 1', max_length=100)
    responsible_2 = forms.CharField(label='Nome do Responsável 2', max_length=100)
    phone = forms.CharField(label='Telefone', max_length=15)
    email = forms.EmailField(label='E-mail')
    ac1 = 'Aceita disponibilizar suas informações para a chefia e diretoria do grupo escoteiro?'
    ac2 = 'Conhece sobre especialidades escoteiras e sua importancia para formação do jovem?'
    ac3 = 'Tem disponibilidade de tempo para avaliar especialidades escoteiras?'
    accept_1 = forms.BooleanField(label=ac1)
    accept_2 = forms.BooleanField(label=ac2)
    accept_3 = forms.BooleanField(label=ac3)


class SkillsModelForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['name_skill','type_skill','name_person','type_person','notes']
    #number_register = forms.CharField(label='Número de Registro', max_length=20)
    name_skill = forms.CharField(label='Nome da Competência', max_length=100)
    type_skill = forms.CharField(widget=forms.Select(choices=types_of_skills), label='Tipo de Habilidade')
    name_person = forms.CharField(label='Nome da Pessoa', max_length=100)
    type_person = forms.CharField(label='Tipo de associação com o escoteiro', max_length=100)
    notes = forms.CharField(label='Anotações', max_length=100)


class SearchForm(forms.Form):
    help_text = 'Digite aqui para pesquisar uma competência, habilidade, hobby ou experiência'
    text_search = forms.CharField(label='Digite aqui o termo para buscar', max_length=100, min_length=0, help_text=help_text, empty_value='')


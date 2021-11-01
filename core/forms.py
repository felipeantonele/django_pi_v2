from django import forms

#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field

from .models import NumbersRegisters, AssociateData


class NrRegisterForm(forms.Form):
    nr = forms.CharField(label='Número de Registro', max_length=20)


class AssociateDataModelForm(forms.ModelForm):
    class Meta:
        model = AssociateData
        fields = ['number_register','name','responsible_1','responsible_2','phone','email','accept_1','accept_2','accept_3']
    number_register = forms.CharField(label='Número de Registro', max_length=20)
    name = forms.CharField(label='Nome do Escoteiro', max_length=100)
    responsible_1 = forms.CharField(label='Nome do Responsável 1', max_length=100)
    responsible_2 = forms.CharField(label='Nome do Responsável 2', max_length=100)
    phone = forms.CharField(label='Telefone', max_length=15)
    email = forms.EmailField(label='E-mail')
    accept_1 = forms.BooleanField(label='accept_1')
    accept_2 = forms.BooleanField(label='accept_2')
    accept_3 = forms.BooleanField(label='accept_3')

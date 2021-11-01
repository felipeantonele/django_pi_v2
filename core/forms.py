from django import forms

#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field

from .models import NumbersRegisters


class NumbersRegistersRegistration(forms.ModelForm):
    class Meta:
        model = NumbersRegisters
        fields = ['number_register', 'function_first', 'function_second', 'function_third', 'section']
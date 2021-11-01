from django.contrib import admin
from .models import AssociateData, Skills, NumbersRegisters
from django.utils.html import format_html


class NumbersRegistersAdmin(admin.ModelAdmin):
    list_display = ('number_register','function_first','function_second','function_third','section') # lista os prdoutos no ADM em formato de tabela com essas colunas


class AssociateDataAdmin(admin.ModelAdmin):
    list_display = ('number_register','name','responsible_1','responsible_2','phone','email','accept_1','accept_2','accept_3')


class SkillsAdmin(admin.ModelAdmin):
    list_display = ('number_register','name_skill','type_skill','name_person','type_person','notes')


admin.site.register(NumbersRegisters, NumbersRegistersAdmin)
admin.site.register(AssociateData, AssociateDataAdmin)
admin.site.register(Skills, SkillsAdmin)


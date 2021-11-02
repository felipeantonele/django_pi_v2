from django.db import models

# Create your models here.


class NumbersRegisters(models.Model):
    number_register = models.CharField('number_register', max_length=20)
    function_first = models.CharField('function_first', max_length=100)
    function_second = models.CharField('function_second', max_length=100)
    function_third = models.CharField('function_third', max_length=100)
    section = models.CharField('section', max_length=100)
    date_creation = models.DateTimeField('date_creation', auto_now_add=True)
    def __str__(self):
        return f'{self.number_register} {self.function_first} {self.section}'


class AssociateData(models.Model):
    number_register = models.CharField('number_register', max_length=20)
    name = models.CharField('name', max_length=100)
    responsible_1 = models.CharField('responsible_1', max_length=100)
    responsible_2 = models.CharField('responsible_2', max_length=100)
    phone = models.CharField('phone', max_length=15)
    email = models.EmailField('email')
    accept_1 = models.BooleanField('accept_1')
    accept_2 = models.BooleanField('accept_2')
    accept_3 = models.BooleanField('accept_3')
    date_creation = models.DateTimeField('date_creation', auto_now_add=True)
    def __str__(self):
        return f'{self.number_register} {self.name}'


class Skills(models.Model):
    number_register = models.CharField('number_register', max_length=20)
    name_skill = models.CharField('name_skill', max_length=100)
    type_skill = models.CharField('type_skill', max_length=100)
    name_person = models.CharField('name_person', max_length=100)
    type_person = models.CharField('type_person', max_length=100)
    notes = models.CharField('notes', max_length=100)
    date_creation = models.DateTimeField('date_creation', auto_now_add=True)
    def __str__(self):
        return f'{self.number_register} {self.name_skill} {self.type_skill}'

    #objects = models.Manager()




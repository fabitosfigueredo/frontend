from django.shortcuts import render
from StoreApp.models import Departamento

def listar_departamentos(request):
    departamentos = Departamento.objects.all()
    context = {
        'departamentos' : departamentos
    }
    return context
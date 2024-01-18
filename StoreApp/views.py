from django.shortcuts import render
from django.core.mail import send_mail
from StoreApp.models import Departamento, Produto
from StoreApp.forms import ContatoForm, ClienteForm

# Create your views here.
def index(request):
    produtos_em_destaque = Produto.objects.filter(destaque = True)

    context = {
        'produtos' : produtos_em_destaque
    }
    return render(request, 'index.html', context)

def produto_lista(request):
    #Buscar produto no banco
    produtos = Produto.objects.all()

    context = {
        'produtos' : produtos,
        'categoria' : 'Todos Produtos',
    }
    return render(request, 'produtos.html', context)

def produto_lista_por_id(request, id):
    #Buscar produto no banco
    produtos = Produto.objects.filter(departamento_id = id)
    #Buscar departamento no banco
    departamento = Departamento.objects.get(id = id)


    context = {
        'produtos' : produtos,
        'categoria' : departamento.nome,
    }
    return render(request, 'produtos.html', context)


def produto_detalhe(request, id):
    #Buscar produto no banco
    produto = Produto.objects.get(id = id)
    produtos_relacionados =  Produto.objects.filter(departamento_id = produto.departamento.id).exclude(id = id)[:4]

    context = {
        'produto' : produto,
        'produtos_relacionados' : produtos_relacionados
    }

    return render(request, 'produto_detalhes.html', context)

def institucional(request):
    return render(request, 'sobre.html')

def contato(request):

    mensagem = ''

    if request.method == 'POST':
        nome = request.POST['nome']
        telefone = request.POST['telefone']
        assunto = request.POST['assunto']
        mensagem = request.POST['mensagem']
        remetente = request.POST['email']
        destinatario = ['fabitofigueredo@gmail.com']
        corpo = f"Nome: {nome} \nTelefone: {telefone} \n Mensagem: {mensagem}"

        
        #fazer envio do e-mail
        try:
            send_mail(assunto, corpo, remetente, destinatario)
            mensagem = 'Mensagem enviada com sucesso'
        except:
            mensagem = 'Erro ao enviar a mensagem'
        

    formulario = ContatoForm()

    context = {
        'form_contato' : formulario,
        'mensagem':  mensagem 
    }
   
    return render(request, 'contato.html', context ) 

def cadastro(request):
    mensagem = ''

    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            mensagem = 'Cliente cadastrado com sucesso'
            formulario = ClienteForm()
        else: 
            mensagem = "Erro ao cadastrar o cliente"    
   
    else:
        formulario = ClienteForm()
    context = {
        'form_cadastro' : formulario,
        'mensagem': mensagem

    }

    return render(request, 'cadastro.html', context)    


from django.shortcuts import render,redirect
from .models import Receita, Despesa, Contas, Categorias
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def home(request):
    return render(request, 'usuarios/home.html')

@login_required
def receitas(request):
    if request.method == 'POST':
        # Criando a nova receita
        nova_receita = Receita()
        nova_receita.data = request.POST.get('data')
        nova_receita.conta = request.POST.get('conta')
        nova_receita.valor = request.POST.get('valor')
        nova_receita.categoria = request.POST.get('categoria')
        nova_receita.observacao = request.POST.get('observacao')
        nova_receita.usuario = request.user  # Associando a receita ao usuário autenticado

        # Salvando no banco de dados
        nova_receita.save()

        # Redirecionando ou renderizando novamente após salvar
        return redirect('receitas')  # Ou renderizar novamente se necessário
    
    contas = Contas.objects.filter(usuario=request.user)  # Pega todas as contas cadastradas
    categorias = Categorias.objects.filter(usuario=request.user,tipo_categoria="Receita")  # Pega todas as categorias cadastradas
    receitas = Receita.objects.filter(usuario=request.user)

    # Caso o método não seja POST, renderize a página normalmente
    return render(request, 'usuarios/receitas.html',{'receitas':receitas,
                                                     'contas':contas,
                                                     'categorias':categorias})

@login_required
def despesas(request):
    if request.method == 'POST':
        # Criando a nova despesa
        nova_despesa = Despesa()
        nova_despesa.data = request.POST.get('data')
        nova_despesa.tipo = request.POST.get('tipo')
        nova_despesa.conta = request.POST.get('conta')
        nova_despesa.vencimento = request.POST.get('vencimento')
        nova_despesa.valor = request.POST.get('valor')
        nova_despesa.categoria = request.POST.get('categoria')
        nova_despesa.observacao = request.POST.get('observacao')
        nova_despesa.usuario = request.user  # Associando a despesa ao usuário autenticado

        # Salvando no banco de dados
        nova_despesa.save()

        # Redirecionando ou renderizando novamente após salvar
        return redirect('despesas')
    
    # Filtrando as despesas para mostrar apenas do usuário autenticado
    despesas = Despesa.objects.filter(usuario=request.user)
    contas = Contas.objects.filter(usuario=request.user)  # Pega todas as contas cadastradas
    categorias = Categorias.objects.filter(usuario=request.user,tipo_categoria="Despesa")  # Pega todas as categorias cadastradas

    return render(request, 'usuarios/despesas.html',{'despesas':despesas,
                                                     'contas':contas,
                                                     'categorias':categorias})

@login_required
def contas(request):

    if request.method == 'POST':
        # Criando a nova conta
        nova_conta = Contas()
        nova_conta.conta = request.POST.get('conta')
        nova_conta.saldo_inicial = request.POST.get('saldo_inicial')
        nova_conta.data_vencimento = request.POST.get('data_vencimento')
        nova_conta.data_fechamento = request.POST.get('data_fechamento')
        nova_conta.usuario = request.user  # Associando a conta ao usuário autenticado
        # Salvando no banco de dados
        nova_conta.save()

        # Redirecionando ou renderizando novamente após salvar
        return redirect('contas')
    contas = Contas.objects.filter(usuario=request.user)  # Filtrando as contas para mostrar apenas do usuário autenticado  
    return render(request, 'usuarios/contas.html',{'contas':contas})

@login_required
def categorias(request):

    if request.method == 'POST':
        # Criando a nova categoria
        nova_categoria = Categorias()
        nova_categoria.categoria = request.POST.get('categoria')
        nova_categoria.tipo_categoria = request.POST.get('tipo_categoria')
        nova_categoria.usuario = request.user  # Associando a categoria ao usuário autenticado
        # Salvando no banco de dados
        nova_categoria.save()

        # Redirecionando ou renderizando novamente após salvar
        return redirect('categorias')
    categorias = Categorias.objects.filter(usuario=request.user)  # Filtrando as categorias para mostrar apenas do usuário autenticado
    return render(request, 'usuarios/categorias.html',{'categorias':categorias})


@login_required
def calcular_fluxo(request):
    fluxo_diario = []  # Inicializa fluxo_diario para evitar erro ao acessar fora do bloco POST
    if request.method == 'POST':
        try:
            # Obtém as datas do formulário (usando valores padrão se não fornecidos)
            data_inicial_str = request.POST.get('data_inicial', '01/01/2025')
            data_final_str = request.POST.get('data_final', '31/12/2025')

            # Verifica se as datas não estão vazias, se estiverem, usa as datas padrão
            if data_inicial_str == '':
                data_inicial_str = '01/01/2025'
            if data_final_str == '':
                data_final_str = '31/12/2025'

            # Converte as datas em formato string para objetos date
            data_inicial = timezone.datetime.strptime(data_inicial_str, "%d/%m/%Y").date()
            data_final = timezone.datetime.strptime(data_final_str, "%d/%m/%Y").date()

            # Filtra as receitas e despesas dentro do intervalo de datas
            receitas = Receita.objects.filter(usuario=request.user,data__gte=data_inicial, data__lte=data_final)
            despesas = Despesa.objects.filter(usuario=request.user,vencimento__gte=data_inicial, vencimento__lte=data_final)

            contas = Contas.objects.filter(usuario=request.user)  # Pega todas as contas cadastradas

            saldo_acumulado = 0  # Inicializa o saldo acumulado
            for conta in contas:
                saldo_acumulado += conta.saldo_inicial

            # Loop para cada dia no intervalo entre data_inicial e data_final
            for dia in (data_inicial + timezone.timedelta(days=i) for i in range((data_final - data_inicial).days + 1)):
                # Recupera as somas para o dia
                total_receitas = receitas.filter(data=dia).aggregate(Sum('valor'))['valor__sum'] or 0
                total_despesas = despesas.filter(data=dia).aggregate(Sum('valor'))['valor__sum'] or 0
                
                # Atualiza o saldo acumulado
                saldo_acumulado += total_receitas - total_despesas

                # Adiciona o resultado ao fluxo diário
                fluxo_diario.append({
                    'data': dia,
                    'total_receitas': total_receitas,
                    'total_despesas': total_despesas,
                    'saldo_acumulado': saldo_acumulado
                })
            
            # Verifica o conteúdo de fluxo_diario
            # print(f"Fluxo Diário: {fluxo_diario}")

            # Passa o fluxo diário calculado para a view
            return render(request, 'usuarios/home.html', {'fluxo_diario': fluxo_diario, 'data_inicial': data_inicial, 'data_final': data_final})

        except Exception as e:
            # Caso ocorra algum erro (como erro de conversão de data), podemos mostrar uma mensagem
            print(f"Erro: {e}")
            return render(request, 'usuarios/home.html', {'fluxo_diario': [], 'data_inicial': None, 'data_final': None})
    else:
        # Se não for um POST, renderiza a página inicial sem dados do fluxo
        print("Não é um POST. Renderizando página inicial.")
        return render(request, 'usuarios/home.html', {'fluxo_diario': fluxo_diario, 'data_inicial': None, 'data_final': None})


@login_required
def remover_despesas(request):
    if request.method == 'POST':
        despesas_ids = request.POST.getlist('despesas')  # Obtém os IDs das despesas selecionadas
        
        # Verificar se a lista de IDs não está vazia e se contém IDs válidos
        if despesas_ids:
            # Filtra as despesas pela lista de IDs e as exclui
            despesas_validas = [id for id in despesas_ids if id.isdigit()]  # Garante que os IDs sejam números válidos
            if despesas_validas:
                Despesa.objects.filter(usuario = request.user,id_despesa__in=despesas_validas).delete()
            else:
                return HttpResponse("Nenhuma despesa válida selecionada.", status=400)
        
        return redirect('despesas')  # Redireciona para a página de despesas após remoção
    
    return HttpResponse(status=400)  # Caso o método não seja POST, retorna erro 400

@login_required
def remover_receitas(request):
    if request.method == 'POST':
        receitas_ids = request.POST.getlist('receitas')  # Obtém os IDs das receitas selecionadas
        
        # Verificar se a lista de IDs não está vazia e se contém IDs válidos
        if receitas_ids:
            # Filtra as receitas pela lista de IDs e as exclui
            receitas_validas = [id for id in receitas_ids if id.isdigit()]  # Garante que os IDs sejam números válidos
            if receitas_validas:
                Receita.objects.filter(usuario = request.user, id_receita__in=receitas_validas).delete()
            else:
                return HttpResponse("Nenhuma receita válida selecionada.", status=400)
        
        return redirect('receitas')  # Redireciona para a página de receitas após remoção
    
    return HttpResponse(status=400)  # Caso o método não seja POST, retorna erro 400

@login_required
def remover_contas(request):
    if request.method == 'POST':
        contas_ids = request.POST.getlist('contas')  # Obtém os IDs das contas selecionadas
        
        # Verificar se a lista de IDs não está vazia e se contém IDs válidos
        if contas_ids:
            # Filtra as contas pela lista de IDs e as exclui
            contas_validas = [id for id in contas_ids if id.isdigit()]  # Garante que os IDs sejam números válidos
            if contas_validas:
                Contas.objects.filter(usuario = request.user,id_conta__in=contas_validas).delete()
            else:
                return HttpResponse("Nenhuma conta válida selecionada.", status=400)
        
        return redirect('contas')  # Redireciona para a página de contas após remoção
    
    return HttpResponse(status=400)  # Caso o método não seja POST, retorna erro 400

@login_required
def remover_categorias(request):
    if request.method == 'POST':
        categorias_ids = request.POST.getlist('categorias')  # Obtém os IDs das categorias selecionadas
        
        # Verificar se a lista de IDs não está vazia e se contém IDs válidos
        if categorias_ids:
            # Filtra as categorias pela lista de IDs e as exclui
            categorias_validas = [id for id in categorias_ids if id.isdigit()]  # Garante que os IDs sejam números válidos
            if categorias_validas:
                Categorias.objects.filter(usuario = request.user,id_categoria__in=categorias_validas).delete()
            else:
                return HttpResponse("Nenhuma categoria válida selecionada.", status=400)
        
        return redirect('categorias')  # Redireciona para a página de categorias após remoção
    
    return HttpResponse(status=400)  # Caso o método não seja POST, retorna erro 400

from django.contrib import admin

# Register your models here.
# usuarios/admin.py
from django.contrib import admin
from .models import Receita, Despesa, Contas, Categorias

# usuarios/admin.py
from django.contrib import admin
from .models import Receita, Despesa, Contas, Categorias

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ( 'data','conta', 'valor', 'categoria')  # Exibe colunas personalizadas na lista
    search_fields = ('data', 'categoria','conta')  # Permite a busca pelos campos data e categoria
    list_filter = ('conta', 'categoria','conta')  # Filtros laterais para facilitar a navegação

class DespesaAdmin(admin.ModelAdmin):
    list_display = ('data', 'conta','tipo','vencimento','valor', 'categoria')  # Exibe colunas personalizadas na lista
    search_fields = ('data', 'categoria','conta', 'tipo')  # Permite a busca pelos campos data e categoria
    list_filter = ('conta', 'categoria','conta', 'tipo')  # Filtros laterais para facilitar a navegação

class ContasAdmin(admin.ModelAdmin):
    list_display = ('conta', 'saldo_inicial','data_vencimento', 'data_fechamento')  # Exibe colunas personalizadas na lista


class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_categoria')  # Exibe colunas personalizadas na lista
    search_fields = ('categoria', 'tipo_categoria')  # Permite a busca pelos campos data e categoria
    list_filter = ('categoria', 'tipo_categoria')  # Filtros laterais para facilitar a navegação


# Registrar o modelo com a personalização
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Despesa,DespesaAdmin)
admin.site.register(Contas,ContasAdmin)
admin.site.register(Categorias,CategoriasAdmin)

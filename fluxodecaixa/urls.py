"""
URL configuration for fluxodecaixa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppFluxoDeCaixa import views
from django.contrib.auth import views as auth_views

#rota, view, referencia
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.calcular_fluxo, name='home'),
    path('receitas/',views.receitas, name='receitas'),
    path('despesas/', views.despesas, name='despesas'),
    path('contas/', views.contas, name='contas'),
    path('categorias/', views.categorias, name='categorias'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('remover_despesas/', views.remover_despesas, name='remover_despesas'),
    path('remover_receitas/', views.remover_receitas, name='remover_receitas'),
    path('remover_contas/', views.remover_contas, name='remover_contas'),
    path('remover_categorias/', views.remover_categorias, name='remover_categorias'),
    path('download-template/excel/', views.download_template_excel, name='download_template_excel'),

]

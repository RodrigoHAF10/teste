from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('os/criar/', views.criar_os, name='criar_os'),
    path('os/<int:os_id>/', views.detalhes_os, name='detalhes_os'),
    path('os/<int:os_id>/alterar/', views.alterar_os, name='alterar_os'),
    path('os/<int:os_id>/excluir/', views.excluir_os, name='excluir_os'),
    path('os/<int:os_id>/atualizar_status/', views.atualizar_status, name='atualizar_status'),
    path('clientes/<int:id>/detalhes/', views.detalhes_cliente, name='detalhes_cliente'),
    path('clientes/<int:id>/alterar/', views.detalhes_cliente, name='alterar_cliente'),
    path('clientes/cadastrar/', views.cadastro_cliente, name='cadastro_cliente'),
    path('clientes/buscar/', views.buscar_cliente, name='buscar_cliente'),
    path('clientes/<int:id>/excluir/', views.excluir_cliente, name='excluir_cliente'),
    path('tecnicos/<int:id>/detalhes/', views.detalhes_tecnico, name='detalhes_tecnico'),
    path('tecnicos/cadastrar/', views.cadastro_tecnico, name='cadastro_tecnico'),
    path('tecnicos/buscar/', views.buscar_tecnico, name='buscar_tecnico'),
    path('tecnicos/<int:id>/excluir/', views.excluir_tecnico, name='excluir_tecnico'),
    path('usuarios/cadastrar/', views.cadastro_usuario, name='cadastro_usuario'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('tecnicos/', views.lista_tecnicos, name='lista_tecnicos'),
]

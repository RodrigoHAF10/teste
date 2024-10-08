from django.contrib import admin
from .models import Cliente, OrdemServico, Tecnico

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'email', 'cnpj', 'cidade', 'estado')
    search_fields = ('nome', 'email', 'telefone', 'cnpj')
    list_filter = ('cidade', 'estado')

class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_completo', 'telefone', 'email')
    search_fields = ('nome_completo', 'email', 'telefone')

class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_criacao', 'hora_criacao', 'data_termino', 'hora_termino', 'status', 'tecnico_responsavel')
    list_filter = ('status', 'data_criacao', 'data_termino')
    search_fields = ('cliente__nome', 'descricao_servico', 'tecnico_responsavel__username')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(OrdemServico, OrdemServicoAdmin)

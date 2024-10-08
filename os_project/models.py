from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=255, default='Desconhecido')
    cnpj = models.CharField(max_length=14, default='00000000000000')
    cep = models.CharField(max_length=8, default='00000000')
    email = models.EmailField(default='email@exemplo.com')
    rua = models.CharField(max_length=255, default='Desconhecido')
    bairro = models.CharField(max_length=255, default='Desconhecido')
    cidade = models.CharField(max_length=255, default='Desconhecida')
    estado = models.CharField(max_length=2, default='SP')
    telefone = models.CharField(max_length=20, default='(00) 00000-0000')
    site = models.URLField(max_length=200, default='http://www.exemplo.com')
    observacoes = models.TextField(default='Sem observações')
    contato = models.CharField(max_length=255, default='Desconhecido')

    def __str__(self):
        return self.nome

class OrdemServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao_servico = models.TextField()
    data_criacao = models.DateField(default=timezone.now)
    hora_criacao = models.TimeField(default=timezone.now)
    data_termino = models.DateField(blank=True, null=True)
    hora_termino = models.TimeField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    tecnico_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('aberto', 'Aberto'), ('concluido', 'Concluído'), ('pendente', 'Pendente')], default='aberto')
    descricao_final = models.TextField(blank=True, null=True)
    km_saida = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    km_chegada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    foto = models.ImageField(upload_to='os_fotos/', blank=True, null=True)

    def __str__(self):
        return f'OS {self.id} - {self.cliente.nome}'

class Tecnico(models.Model):
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome_completo

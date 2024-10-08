from django import forms
from .models import Cliente, OrdemServico, Tecnico

class OrdemServicoForm(forms.ModelForm):
    data_criacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora_criacao = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    data_termino = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    hora_termino = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = OrdemServico
        fields = [
            'cliente', 'descricao_servico', 'data_criacao', 'hora_criacao', 
            'data_termino', 'hora_termino', 'observacoes', 
            'tecnico_responsavel', 'status'
        ]

class CriarOSForm(forms.ModelForm):
    tecnico_responsavel = forms.ModelChoiceField(
        queryset=Tecnico.objects.all(),
        required=False,
        label="Técnico Responsável",
        widget=forms.Select
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True,
        label="Cliente",
        widget=forms.Select
    )

    class Meta:
        model = OrdemServico
        fields = ['cliente', 'descricao_servico', 'observacoes', 'tecnico_responsavel']

    def __init__(self, *args, **kwargs):
        super(CriarOSForm, self).__init__(*args, **kwargs)
        self.fields['tecnico_responsavel'].queryset = Tecnico.objects.all()
        self.fields['tecnico_responsavel'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome_completo}"
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome}"

class AlterarOSForm(forms.ModelForm):
    tecnico_responsavel = forms.ModelChoiceField(
        queryset=Tecnico.objects.all(),
        required=False,
        label="Técnico Responsável",
        widget=forms.Select
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True,
        label="Cliente",
        widget=forms.Select
    )

    class Meta:
        model = OrdemServico
        fields = [
            'cliente', 'descricao_servico', 'observacoes', 'tecnico_responsavel', 
            'data_termino', 'hora_termino', 'descricao_final', 'km_saida', 
            'km_chegada', 'foto'
        ]

    def __init__(self, *args, **kwargs):
        super(AlterarOSForm, self).__init__(*args, **kwargs)
        self.fields['tecnico_responsavel'].queryset = Tecnico.objects.all()
        self.fields['tecnico_responsavel'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome_completo}"
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome}"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome', 'cnpj', 'cep', 'email', 'rua', 'bairro', 
            'cidade', 'estado', 'telefone', 'site', 'observacoes', 'contato'
        ]

class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = ['nome_completo', 'telefone', 'email']

class HomeSearchForm(forms.Form):
    SEARCH_OPTIONS = [
        ('os', 'Ordem de Serviço'),
        ('cliente', 'Cliente'),
        ('data_criacao', 'Data de Criação'),
        ('hora_criacao', 'Hora de Criação'),
        ('data_termino', 'Data de Término'),
        ('hora_termino', 'Hora de Término'),
        ('status', 'Status'),
        ('tecnico', 'Técnico Responsável'),
    ]

    search_field = forms.CharField(required=False, label='Termo de Busca')
    search_option = forms.ChoiceField(choices=SEARCH_OPTIONS, required=False, label='Opção de Busca')
    search_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data')
    search_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora')

class ClienteSearchForm(forms.Form):
    SEARCH_OPTIONS = [
        ('id', 'ID'),
        ('nome', 'Nome'),
        ('telefone', 'Telefone'),
        ('email', 'Email'),
    ]

    search_field = forms.CharField(max_length=100, required=False)
    search_option = forms.ChoiceField(choices=SEARCH_OPTIONS, required=False)

class TecnicoSearchForm(forms.Form):
    SEARCH_OPTIONS = [
        ('id', 'ID'),
        ('nome', 'Nome'),
        ('telefone', 'Telefone'),
        ('email', 'Email'),
    ]

    search_field = forms.CharField(max_length=100, required=False)
    search_option = forms.ChoiceField(choices=SEARCH_OPTIONS, required=False)
